import json
from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reservations.models import Booking, Court
from reservations.services import create_booking


User = get_user_model()


class ReservationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="marina", email="marina@example.com", password="Reserva-Segura-2026!")
        self.other = User.objects.create_user(username="lucas", email="lucas@example.com", password="Reserva-Segura-2026!")
        self.court = Court.objects.create(
            name="Cancha Pacífico",
            description="Pádel techado",
            location="Costa del Este",
            opening_time=time(8, 0),
            closing_time=time(20, 0),
            slot_minutes=60,
        )
        self.inactive = Court.objects.create(
            name="Cancha cerrada",
            opening_time=time(8, 0),
            closing_time=time(20, 0),
            is_active=False,
        )
        day = timezone.localdate() + timedelta(days=4)
        self.start = timezone.make_aware(datetime.combine(day, time(10, 0)), timezone.get_current_timezone())
        self.end = self.start + timedelta(hours=1)

    def test_home_lists_only_active_courts(self):
        response = self.client.get(reverse("reservations:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancha Pacífico")
        self.assertNotContains(response, "Cancha cerrada")

    def test_registration_creates_normalized_user_and_logs_in(self):
        response = self.client.post(
            reverse("reservations:register"),
            {
                "username": "nuevo",
                "first_name": "Nora",
                "last_name": "Díaz",
                "email": "NORA@EXAMPLE.COM",
                "password1": "Reserva-Segura-2026!",
                "password2": "Reserva-Segura-2026!",
            },
        )

        self.assertRedirects(response, reverse("reservations:home"))
        user = User.objects.get(username="nuevo")
        self.assertEqual(user.email, "nora@example.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_registration_rejects_duplicate_email(self):
        response = self.client.post(
            reverse("reservations:register"),
            {
                "username": "otro_nombre",
                "first_name": "Otra",
                "last_name": "Persona",
                "email": "MARINA@EXAMPLE.COM",
                "password1": "Reserva-Segura-2026!",
                "password2": "Reserva-Segura-2026!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con este correo electrónico")

    def test_calendar_contains_month_grid_slots_and_summary(self):
        response = self.client.get(reverse("reservations:booking_calendar", args=[self.court.pk]))

        self.assertContains(response, 'id="calendar-grid"')
        self.assertContains(response, 'id="slot-grid"')
        self.assertContains(response, "Tu reserva")
        self.assertContains(response, "Hora de Panamá")

    def test_availability_api_returns_open_slots(self):
        response = self.client.get(
            reverse("reservations:availability_api", args=[self.court.pk]),
            {"date": self.start.date().isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()["slots"]), 5)
        self.assertEqual(response.json()["court"]["name"], "Cancha Pacífico")

    def test_booking_api_requires_authentication(self):
        response = self.client.post(
            reverse("reservations:create_booking_api"),
            data=json.dumps({"court_id": self.court.pk, "starts_at": self.start.isoformat(), "ends_at": self.end.isoformat()}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["code"], "authentication_required")

    def test_authenticated_user_can_create_booking(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("reservations:create_booking_api"),
            data=json.dumps({"court_id": self.court.pk, "starts_at": self.start.isoformat(), "ends_at": self.end.isoformat()}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Booking.objects.filter(user=self.user, court=self.court).exists())

    def test_conflict_returns_clear_error_and_alternatives(self):
        create_booking(user=self.other, court=self.court, starts_at=self.start, ends_at=self.end)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("reservations:create_booking_api"),
            data=json.dumps({"court_id": self.court.pk, "starts_at": self.start.isoformat(), "ends_at": self.end.isoformat()}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["code"], "booking_rejected")
        self.assertIn("reservado", response.json()["error"])
        self.assertTrue(response.json()["alternatives"])
        self.assertEqual(Booking.objects.count(), 1)

    def test_my_bookings_does_not_show_another_users_reservation(self):
        own = create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)
        other_start = self.end + timedelta(hours=1)
        other = create_booking(user=self.other, court=self.court, starts_at=other_start, ends_at=other_start + timedelta(hours=1))
        self.client.force_login(self.user)

        response = self.client.get(reverse("reservations:my_bookings"))

        self.assertContains(response, reverse("reservations:cancel_booking", args=[own.pk]))
        self.assertNotContains(response, reverse("reservations:cancel_booking", args=[other.pk]))

    def test_user_can_cancel_own_booking(self):
        booking = create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)
        self.client.force_login(self.user)

        response = self.client.post(reverse("reservations:cancel_booking", args=[booking.pk]))

        self.assertRedirects(response, reverse("reservations:my_bookings"))
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CANCELLED)

    def test_cancel_endpoint_rejects_get(self):
        booking = create_booking(user=self.user, court=self.court, starts_at=self.start, ends_at=self.end)
        self.client.force_login(self.user)

        response = self.client.get(reverse("reservations:cancel_booking", args=[booking.pk]))

        self.assertEqual(response.status_code, 405)

