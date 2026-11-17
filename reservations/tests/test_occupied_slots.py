from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reservations.models import Booking, Court, CourtBlock
from reservations.services import available_slots, cancel_booking, create_booking, day_availability


User = get_user_model()


class OccupiedSlotsTests(TestCase):
    """HU-03 / CA-01 / CA-14: la jornada muestra horarios disponibles y ocupados."""

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="cliente_privado", email="privado@example.com", password="Reserva-Segura-2026!"
        )
        self.admin = User.objects.create_user(username="admin", password="Reserva-Segura-2026!", is_staff=True)
        self.court = Court.objects.create(
            name="Cancha Pacífico",
            opening_time=time(8, 0),
            closing_time=time(12, 0),
            slot_minutes=60,
        )
        self.day = timezone.localdate() + timedelta(days=3)
        self.zone = timezone.get_current_timezone()

    def at(self, hour):
        return timezone.make_aware(datetime.combine(self.day, time(hour, 0)), self.zone)

    def availability(self):
        response = self.client.get(
            reverse("reservations:availability_api", args=[self.court.pk]), {"date": self.day.isoformat()}
        )
        self.assertEqual(response.status_code, 200)
        return response

    def test_booked_slot_is_reported_as_occupied_not_available(self):
        create_booking(user=self.client_user, court=self.court, starts_at=self.at(9), ends_at=self.at(10))

        payload = self.availability().json()

        self.assertEqual([slot["start"] for slot in payload["occupied_slots"]], [self.at(9).isoformat()])
        self.assertNotIn(self.at(9).isoformat(), [slot["start"] for slot in payload["slots"]])
        self.assertEqual(len(payload["slots"]) + len(payload["occupied_slots"]), 4)

    def test_block_is_reported_as_occupied_without_reason(self):
        CourtBlock.objects.create(
            court=self.court, starts_at=self.at(10), ends_at=self.at(12), reason="Mantenimiento secreto", created_by=self.admin
        )

        response = self.availability()

        self.assertEqual(
            [slot["start"] for slot in response.json()["occupied_slots"]],
            [self.at(10).isoformat(), self.at(11).isoformat()],
        )
        self.assertNotContains(response, "Mantenimiento secreto")

    def test_occupied_slots_do_not_reveal_customer_identity(self):
        create_booking(user=self.client_user, court=self.court, starts_at=self.at(8), ends_at=self.at(9))

        response = self.availability()

        self.assertEqual(set(response.json()["occupied_slots"][0]), {"start", "end", "label"})
        self.assertNotContains(response, "cliente_privado")
        self.assertNotContains(response, "privado@example.com")

    def test_cancelled_booking_frees_the_slot(self):
        booking = create_booking(user=self.client_user, court=self.court, starts_at=self.at(9), ends_at=self.at(10))
        cancel_booking(booking=booking, actor=self.client_user)

        payload = self.availability().json()

        self.assertEqual(payload["occupied_slots"], [])
        self.assertEqual(len(payload["slots"]), 4)

    def test_past_slots_are_not_listed_as_occupied(self):
        today = timezone.localdate()
        past_start = timezone.make_aware(datetime.combine(today - timedelta(days=1), time(9, 0)), self.zone)
        Booking.objects.create(user=self.client_user, court=self.court, starts_at=past_start, ends_at=past_start + timedelta(hours=1))

        available, occupied = day_availability(court=self.court, day=past_start.date())

        self.assertEqual((available, occupied), ([], []))

    def test_available_slots_keeps_its_original_contract(self):
        create_booking(user=self.client_user, court=self.court, starts_at=self.at(9), ends_at=self.at(10))

        slots = available_slots(court=self.court, day=self.day)

        self.assertEqual(set(slots[0]), {"start", "end", "label"})
        self.assertEqual(len(slots), 3)

    def test_query_count_does_not_grow_with_number_of_slots(self):
        long_court = Court.objects.create(
            name="Cancha Larga", opening_time=time(6, 0), closing_time=time(23, 0), slot_minutes=30
        )
        create_booking(user=self.client_user, court=long_court, starts_at=self.at(9), ends_at=self.at(10))

        with self.assertNumQueries(2):
            day_availability(court=self.court, day=self.day)
        with self.assertNumQueries(2):
            available, occupied = day_availability(court=long_court, day=self.day)

        self.assertEqual(len(available) + len(occupied), 34)
        self.assertEqual(len(occupied), 2)
