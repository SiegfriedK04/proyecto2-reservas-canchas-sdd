from datetime import datetime, timedelta

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from .models import AuditEvent, Booking, Court, CourtBlock


CANCELLATION_NOTICE = timedelta(hours=2)


@transaction.atomic
def create_booking(*, user, court, starts_at, ends_at):
    locked_court = Court.objects.select_for_update().get(pk=court.pk)
    booking = Booking(user=user, court=locked_court, starts_at=starts_at, ends_at=ends_at)
    booking.full_clean()
    booking.save()
    AuditEvent.objects.create(
        actor=user,
        event_type="booking_created",
        entity_type="booking",
        entity_id=booking.pk,
        details={"court_id": locked_court.pk},
    )
    return booking


@transaction.atomic
def cancel_booking(*, booking, actor):
    locked = Booking.objects.select_for_update().select_related("court", "user").get(pk=booking.pk)
    if actor != locked.user and not actor.is_staff:
        raise PermissionDenied("No puede cancelar una reserva ajena.")
    if locked.status != Booking.Status.CONFIRMED:
        raise ValidationError("La reserva ya no está activa.")
    if not actor.is_staff and locked.starts_at < timezone.now() + CANCELLATION_NOTICE:
        raise ValidationError("La cancelación requiere al menos dos horas de anticipación.")

    locked.status = Booking.Status.CANCELLED
    locked.cancelled_at = timezone.now()
    locked.save(update_fields=("status", "cancelled_at"))
    AuditEvent.objects.create(
        actor=actor,
        event_type="booking_cancelled",
        entity_type="booking",
        entity_id=locked.pk,
        details={"court_id": locked.court_id},
    )
    return locked


def can_cancel_booking(*, booking, actor):
    if booking.status != Booking.Status.CONFIRMED:
        return False
    return actor.is_staff or booking.starts_at >= timezone.now() + CANCELLATION_NOTICE


def day_schedule(*, court, day):
    """Horarios futuros de la jornada, marcados como disponibles u ocupados.

    Reservas confirmadas y bloqueos se consultan una sola vez para toda la
    jornada. Un horario ocupado no informa usuario ni motivo (RN-10).
    """
    zone = timezone.get_current_timezone()
    opening = timezone.make_aware(datetime.combine(day, court.opening_time), zone)
    closing = timezone.make_aware(datetime.combine(day, court.closing_time), zone)
    duration = timedelta(minutes=court.slot_minutes)
    busy = list(
        court.bookings.filter(
            status=Booking.Status.CONFIRMED, starts_at__lt=closing, ends_at__gt=opening
        ).values_list("starts_at", "ends_at")
    )
    busy += list(court.blocks.filter(starts_at__lt=closing, ends_at__gt=opening).values_list("starts_at", "ends_at"))
    now = timezone.now()
    schedule = []

    cursor = opening
    while cursor + duration <= closing:
        slot_end = cursor + duration
        if cursor > now:
            occupied = any(start < slot_end and end > cursor for start, end in busy)
            schedule.append(
                {
                    "start": cursor.isoformat(),
                    "end": slot_end.isoformat(),
                    "label": timezone.localtime(cursor).strftime("%I:%M %p").lstrip("0").lower(),
                    "available": not occupied,
                }
            )
        cursor = slot_end
    return schedule


def day_availability(*, court, day):
    """Devuelve (disponibles, ocupados) con una sola lectura de la jornada."""
    available, occupied = [], []
    for slot in day_schedule(court=court, day=day):
        public = {"start": slot["start"], "end": slot["end"], "label": slot["label"]}
        (available if slot["available"] else occupied).append(public)
    return available, occupied


def available_slots(*, court, day):
    return day_availability(court=court, day=day)[0]


def nearest_alternatives(*, court, starts_at, ends_at, limit=4):
    day_slots = available_slots(court=court, day=timezone.localtime(starts_at).date())
    requested_duration = ends_at - starts_at
    matching = []
    for slot in day_slots:
        slot_start = datetime.fromisoformat(slot["start"])
        slot_end = datetime.fromisoformat(slot["end"])
        if slot_end - slot_start == requested_duration:
            matching.append(slot)
    return matching[:limit]

