from datetime import datetime, timedelta

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from .models import AuditEvent, Booking, Court, CourtBlock


def _intersects(queryset, starts_at, ends_at):
    return queryset.filter(starts_at__lt=ends_at, ends_at__gt=starts_at).exists()


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


def available_slots(*, court, day):
    zone = timezone.get_current_timezone()
    cursor = timezone.make_aware(datetime.combine(day, court.opening_time), zone)
    closing = timezone.make_aware(datetime.combine(day, court.closing_time), zone)
    duration = timedelta(minutes=court.slot_minutes)
    bookings = court.bookings.filter(status=Booking.Status.CONFIRMED)
    blocks = court.blocks.all()
    slots = []

    while cursor + duration <= closing:
        slot_end = cursor + duration
        if cursor > timezone.now() and not _intersects(bookings, cursor, slot_end) and not _intersects(blocks, cursor, slot_end):
            slots.append(
                {
                    "start": cursor.isoformat(),
                    "end": slot_end.isoformat(),
                    "label": timezone.localtime(cursor).strftime("%I:%M %p").lstrip("0").lower(),
                }
            )
        cursor = slot_end
    return slots


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

