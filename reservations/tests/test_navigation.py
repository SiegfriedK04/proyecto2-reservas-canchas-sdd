from datetime import time
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from reservations.models import Court


User = get_user_model()


class AccessibleNavigationTests(TestCase):
    """HU-10 / CA-12: navegación disponible en móvil y con teclado."""

    def setUp(self):
        self.user = User.objects.create_user(username="marina", password="Reserva-Segura-2026!")
        self.court = Court.objects.create(name="Cancha Pacífico", opening_time=time(8, 0), closing_time=time(20, 0))

    def test_every_page_offers_skip_link_to_main_content(self):
        response = self.client.get(reverse("reservations:home"))

        self.assertContains(response, 'class="skip-link" href="#contenido"')
        self.assertContains(response, '<main id="contenido"')

    def test_home_link_is_marked_as_current_page(self):
        response = self.client.get(reverse("reservations:home"))

        self.assertContains(response, f'<a href="{reverse("reservations:home")}" aria-current="page">Canchas</a>', html=True)
        self.assertContains(response, 'aria-current="page"', count=1)

    def test_my_bookings_link_is_marked_as_current_page(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("reservations:my_bookings"))

        self.assertContains(
            response,
            f'<a href="{reverse("reservations:my_bookings")}" aria-current="page">Mis reservas</a>',
            html=True,
        )
        self.assertContains(response, 'aria-current="page"', count=1)

    def test_calendar_page_does_not_mark_a_menu_item(self):
        response = self.client.get(reverse("reservations:booking_calendar", args=[self.court.pk]))

        self.assertNotContains(response, 'aria-current="page"')

    def test_authenticated_navigation_keeps_account_actions(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("reservations:home"))

        self.assertContains(response, "Mis reservas")
        self.assertContains(response, "Cerrar sesión")

    def test_mobile_styles_do_not_hide_account_links(self):
        css = (Path(settings.BASE_DIR) / "static" / "css" / "app.css").read_text(encoding="utf-8")

        self.assertNotIn(".nav-links > a:not(.button), .nav-links form { display: none; }", css)
        self.assertIn(":focus-visible", css)
