from io import StringIO

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from reservations.models import AuditEvent, Booking, Court, CourtBlock


User = get_user_model()


class DemoDataTests(TestCase):
    def test_demo_command_is_repeatable(self):
        output = StringIO()
        call_command("crear_datos_demo", stdout=output)
        call_command("crear_datos_demo", stdout=output)

        self.assertEqual(Court.objects.count(), 3)
        self.assertEqual(Booking.objects.count(), 3)
        self.assertEqual(CourtBlock.objects.count(), 1)
        self.assertEqual(User.objects.filter(username__in=("admin_user", "demo_user")).count(), 2)

    def test_demo_administrator_has_expected_permissions(self):
        call_command("crear_datos_demo", stdout=StringIO())

        administrator = User.objects.get(username="admin_user")
        self.assertTrue(administrator.is_staff)
        self.assertTrue(administrator.is_superuser)
        self.assertTrue(administrator.check_password("admin1234"))


class AdministrationTests(TestCase):
    def test_operational_models_are_available_in_admin(self):
        for model in (Court, Booking, CourtBlock, AuditEvent):
            with self.subTest(model=model.__name__):
                self.assertIn(model, admin.site._registry)
