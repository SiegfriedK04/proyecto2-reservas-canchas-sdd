from datetime import date, datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.utils import timezone

from reservations.models import AuditEvent, Booking, Court, CourtBlock
from reservations.services import available_slots, cancel_booking, create_booking


User = get_user_model()


class BookingCoreTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cliente", password="Reserva-Segura-2026!")
        self.other = User.objects.create_user(username="otro", password="Reserva-Segura-2026!")
        self.admin = User.objects.create_user(username="admin", password="Reserva-Segura-2026!", is_staff=True)
        self.court = Court.objects.create(
            name="Cancha Pacífico",
            description="Cancha techada",
            location="Ciudad de Panamá",
            opening_time=time(8, 0),
            closing_time=time(20, 0),
            slot_minutes=60,
        )
        future_day = timezone.localdate() + timedelta(days=5)
        zone = timezone.get_current_timezone()
        self.start = timezone.make_aware(datetime.combine(future_day, time(10, 0)), zone)
        self.end = self.start + timedelta(hours=1)

    def test_create_booking_adds_audit_event(self):
        booking = create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        self.assertEqual(booking.status, Booking.Status.CONFIRMED)
        event = AuditEvent.objects.get(entity_id=booking.pk)
        self.assertEqual(event.event_type, "booking_created")
        self.assertEqual(event.actor, self.user)

    def test_exact_double_booking_is_rejected_without_partial_write(self):
        create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        with self.assertRaises(ValidationError):
            create_booking(user=self.other, court=self.court, starts_at=self.start, ends_at=self.end)

        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(AuditEvent.objects.filter(event_type="booking_created").count(), 1)

    def test_partial_overlap_is_rejected(self):
        create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        with self.assertRaises(ValidationError):
            create_booking(
                user=self.other,
                court=self.court,
                starts_at=self.start + timedelta(minutes=30),
                ends_at=self.end + timedelta(minutes=30),
            )

    def test_consecutive_intervals_are_allowed(self):
        create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        second = create_booking(
            user=self.other,
            court=self.court,
            starts_at=self.end,
            ends_at=self.end + timedelta(hours=1),
        )

        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(second.starts_at, self.end)

    def test_administrative_block_rejects_booking(self):
        CourtBlock.objects.create(
            court=self.court,
            starts_at=self.start,
            ends_at=self.end,
            reason="Mantenimiento",
            created_by=self.admin,
        )

        with self.assertRaises(ValidationError):
            create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        self.assertFalse(Booking.objects.exists())

    def test_past_booking_is_rejected(self):
        past_start = timezone.now() - timedelta(hours=2)

        with self.assertRaises(ValidationError):
            create_booking(
                user=self.user,
                court=self.court,
                starts_at=past_start,
                ends_at=past_start + timedelta(hours=1),
            )

    def test_outside_operating_hours_is_rejected(self):
        early = self.start.replace(hour=7)

        with self.assertRaises(ValidationError):
            create_booking(user=self.user, court=self.court, starts_at=early, ends_at=early + timedelta(hours=1))

    def test_owner_can_cancel_and_audit_is_preserved(self):
        booking = create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        result = cancel_booking(booking=booking, actor=self.user)

        self.assertEqual(result.status, Booking.Status.CANCELLED)
        self.assertIsNotNone(result.cancelled_at)
        self.assertTrue(AuditEvent.objects.filter(event_type="booking_cancelled", entity_id=booking.pk).exists())

    def test_user_cannot_cancel_another_users_booking(self):
        booking = create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        with self.assertRaises(PermissionDenied):
            cancel_booking(booking=booking, actor=self.other)

        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CONFIRMED)

    def test_staff_can_cancel_for_operations(self):
        booking = create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)

        result = cancel_booking(booking=booking, actor=self.admin)

        self.assertEqual(result.status, Booking.Status.CANCELLED)

    def test_customer_cannot_cancel_with_less_than_two_hours_notice(self):
        starts_at = timezone.now() + timedelta(hours=1)
        booking = Booking.objects.create(
            user=self.user,
            court=self.court,
            starts_at=starts_at,
            ends_at=starts_at + timedelta(hours=1),
        )

        with self.assertRaisesMessage(ValidationError, "dos horas"):
            cancel_booking(booking=booking, actor=self.user)

        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CONFIRMED)

    def test_available_slots_exclude_booking_and_block(self):
        day = self.start.date()
        create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)
        CourtBlock.objects.create(
            court=self.court,
            starts_at=self.end,
            ends_at=self.end + timedelta(hours=1),
            reason="Clase",
            created_by=self.admin,
        )

        slots = available_slots(court=self.court, day=day)
        starts = {slot["start"] for slot in slots}

        self.assertNotIn(self.start.isoformat(), starts)
        self.assertNotIn(self.end.isoformat(), starts)
        self.assertIn(self.end.replace(hour=12).isoformat(), starts)


class CourtValidationTests(TestCase):
    def test_court_requires_valid_hours(self):
        court = Court(name="Inválida", opening_time=time(20, 0), closing_time=time(8, 0), slot_minutes=60)

        with self.assertRaises(ValidationError):
            court.full_clean()

    def test_court_rejects_unsupported_slot_duration(self):
        court = Court(name="Inválida", opening_time=time(8, 0), closing_time=time(20, 0), slot_minutes=17)

        with self.assertRaises(ValidationError):
            court.full_clean()

