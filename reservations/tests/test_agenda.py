from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reservations.models import Booking, Court
from reservations.services import cancel_booking, create_booking


User = get_user_model()


class OrganizedAgendaTests(TestCase):
    """HU-11 / CA-13: agenda con próxima reserva, próximas e historial."""

    def setUp(self):
        self.user = User.objects.create_user(username="marina", password="Reserva-Segura-2026!")
        self.other = User.objects.create_user(username="lucas", password="Reserva-Segura-2026!")
        self.court = Court.objects.create(
            name="Cancha Pacífico", location="Costa del Este", opening_time=time(8, 0), closing_time=time(20, 0)
        )
        self.zone = timezone.get_current_timezone()
        self.client.force_login(self.user)

    def book(self, days, hour=10, user=None):
        start = timezone.make_aware(datetime.combine(timezone.localdate() + timedelta(days=days), time(hour, 0)), self.zone)
        return create_booking(user=user or self.user, court=self.court, starts_at=start, ends_at=start + timedelta(hours=1))

    def past_booking(self, days_ago):
        start = timezone.now() - timedelta(days=days_ago)
        return Booking.objects.create(user=self.user, court=self.court, starts_at=start, ends_at=start + timedelta(hours=1))

    def agenda(self):
        return self.client.get(reverse("reservations:my_bookings"))

    def test_upcoming_bookings_are_sorted_soonest_first(self):
        later = self.book(days=6)
        sooner = self.book(days=2)
        middle = self.book(days=4)

        response = self.agenda()

        self.assertEqual(list(response.context["upcoming"]), [sooner, middle, later])

    def test_next_booking_is_highlighted_as_reminder(self):
        self.book(days=6)
        sooner = self.book(days=2)

        response = self.agenda()

        self.assertEqual(response.context["next_booking"], sooner)
        self.assertContains(response, "Tu próxima reserva")
        self.assertContains(response, "Comienza en")

    def test_finished_booking_goes_to_history_without_late_cancellation_note(self):
        finished = self.past_booking(days_ago=1)

        response = self.agenda()

        self.assertEqual(list(response.context["history"]), [finished])
        self.assertEqual(response.context["upcoming"], [])
        self.assertContains(response, "Finalizada")
        self.assertNotContains(response, "Faltan menos de dos horas")
        self.assertNotContains(response, "Tu próxima reserva")

    def test_cancelled_booking_appears_only_in_history(self):
        booking = self.book(days=3)
        cancel_booking(booking=booking, actor=self.user)

        response = self.agenda()

        self.assertEqual(response.context["upcoming"], [])
        self.assertEqual(list(response.context["history"]), [booking])
        self.assertContains(response, "Cancelada")

    def test_history_is_sorted_most_recent_first(self):
        older = self.past_booking(days_ago=5)
        recent = self.past_booking(days_ago=1)

        response = self.agenda()

        self.assertEqual(list(response.context["history"]), [recent, older])

    def test_cancel_form_asks_for_confirmation(self):
        booking = self.book(days=3)

        response = self.agenda()

        self.assertContains(response, reverse("reservations:cancel_booking", args=[booking.pk]))
        self.assertContains(response, "window.confirm(")

    def test_agenda_excludes_other_users_bookings(self):
        self.book(days=3, user=self.other)

        response = self.agenda()

        self.assertEqual(response.context["upcoming"], [])
        self.assertEqual(response.context["history"], [])
        self.assertContains(response, "Aún no tienes reservas")
