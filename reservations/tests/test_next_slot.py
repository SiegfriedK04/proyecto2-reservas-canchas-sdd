from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reservations.models import Court, CourtBlock
from reservations.services import create_booking, next_available_slot


User = get_user_model()


class NextAvailableSlotTests(TestCase):
    """HU-12 / CA-15 / RF-14: próximo horario real y fecha inicial del calendario."""

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="Reserva-Segura-2026!", is_staff=True)
        self.client_user = User.objects.create_user(username="cliente", password="Reserva-Segura-2026!")
        self.zone = timezone.get_current_timezone()
        self.today = timezone.localdate()
        self.early = Court.objects.create(name="Arena Temprana", opening_time=time(8, 0), closing_time=time(20, 0))
        self.late = Court.objects.create(name="Club Tardío", opening_time=time(10, 0), closing_time=time(20, 0))

    def at(self, days, hour):
        return timezone.make_aware(datetime.combine(self.today + timedelta(days=days), time(hour, 0)), self.zone)

    def block_days(self, court, days):
        CourtBlock.objects.create(
            court=court, starts_at=self.at(0, 0), ends_at=self.at(days, 0), reason="Torneo", created_by=self.admin
        )

    def test_returns_earliest_slot_across_active_courts(self):
        self.block_days(self.early, 2)
        self.block_days(self.late, 2)

        slot = next_available_slot()

        self.assertEqual(slot["court"], self.early)
        self.assertEqual(slot["starts_at"], self.at(2, 8))
        self.assertEqual(slot["day"], self.today + timedelta(days=2))

    def test_respects_existing_bookings(self):
        self.block_days(self.early, 2)
        self.block_days(self.late, 2)
        create_booking(user=self.client_user, court=self.early, starts_at=self.at(2, 8), ends_at=self.at(2, 9))

        slot = next_available_slot()

        self.assertEqual((slot["court"], slot["starts_at"]), (self.early, self.at(2, 9)))

    def test_ignores_inactive_courts(self):
        self.block_days(self.late, 2)
        self.early.is_active = False
        self.early.save()

        slot = next_available_slot()

        self.assertEqual(slot["court"], self.late)

    def test_returns_none_when_nothing_is_free_within_the_window(self):
        self.block_days(self.early, 8)
        self.block_days(self.late, 8)

        self.assertIsNone(next_available_slot())

    def test_home_shows_real_slot_with_calendar_link(self):
        self.block_days(self.early, 2)
        self.block_days(self.late, 2)

        response = self.client.get(reverse("reservations:home"))

        target_day = (self.today + timedelta(days=2)).isoformat()
        link = f'{reverse("reservations:booking_calendar", args=[self.early.pk])}?fecha={target_day}'
        self.assertContains(response, link)
        self.assertContains(response, "Próximo horario libre")
        self.assertNotContains(response, "6:30 p. m.")

    def test_home_shows_neutral_message_without_slots(self):
        self.block_days(self.early, 8)
        self.block_days(self.late, 8)

        response = self.client.get(reverse("reservations:home"))

        self.assertContains(response, "Consulta el calendario")
        self.assertNotContains(response, "Próximo horario libre")

    def test_calendar_uses_valid_future_date_parameter(self):
        target = (self.today + timedelta(days=5)).isoformat()

        response = self.client.get(reverse("reservations:booking_calendar", args=[self.early.pk]), {"fecha": target})

        self.assertEqual(response.context["initial_date"], target)

    def test_calendar_ignores_past_or_invalid_date_parameter(self):
        default = (self.today + timedelta(days=1)).isoformat()
        url = reverse("reservations:booking_calendar", args=[self.early.pk])

        for value in ((self.today - timedelta(days=1)).isoformat(), "no-es-fecha", "2026-13-40"):
            with self.subTest(fecha=value):
                response = self.client.get(url, {"fecha": value})
                self.assertEqual(response.context["initial_date"], default)
