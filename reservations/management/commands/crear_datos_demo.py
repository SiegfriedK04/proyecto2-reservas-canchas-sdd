from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from reservations.models import Booking, Court, CourtBlock
from reservations.services import create_booking


User = get_user_model()


class Command(BaseCommand):
    help = "Crea usuarios, canchas y reservas variadas para la demostración local."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username="admin_user", defaults={"email": "admin@example.local"})
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("admin1234")
        admin.save()

        demo, _ = User.objects.get_or_create(
            username="demo_user",
            defaults={"first_name": "Marina", "last_name": "Santos", "email": "demo@example.local"},
        )
        demo.set_password("demo1234")
        demo.save()

        courts_data = [
            {
                "name": "Cancha Pacífico",
                "description": "Cancha de pádel techada con iluminación uniforme y área de descanso.",
                "location": "Sede Costa del Este",
                "opening_time": time(8, 0),
                "closing_time": time(21, 0),
                "slot_minutes": 60,
            },
            {
                "name": "Arena Alba",
                "description": "Superficie multipropósito para tenis y entrenamiento individual.",
                "location": "Sede Obarrio",
                "opening_time": time(7, 0),
                "closing_time": time(20, 0),
                "slot_minutes": 60,
            },
            {
                "name": "Club Costa",
                "description": "Cancha abierta con gradería compacta y ventilación natural.",
                "location": "Sede San Francisco",
                "opening_time": time(9, 0),
                "closing_time": time(22, 0),
                "slot_minutes": 60,
            },
        ]
        courts = []
        for data in courts_data:
            court, _ = Court.objects.update_or_create(name=data["name"], defaults=data)
            courts.append(court)

        zone = timezone.get_current_timezone()
        first_day = timezone.localdate() + timedelta(days=1)
        for index, court in enumerate(courts):
            start = timezone.make_aware(datetime.combine(first_day + timedelta(days=index), time(10 + index, 0)), zone)
            if not Booking.objects.filter(court=court, starts_at=start).exists():
                create_booking(user=demo, court=court, starts_at=start, ends_at=start + timedelta(hours=1))

        block_start = timezone.make_aware(datetime.combine(first_day + timedelta(days=2), time(15, 0)), zone)
        CourtBlock.objects.get_or_create(
            court=courts[0],
            starts_at=block_start,
            ends_at=block_start + timedelta(hours=2),
            defaults={"reason": "Mantenimiento preventivo", "created_by": admin},
        )

        self.stdout.write(self.style.SUCCESS("Datos de demostración listos."))
        self.stdout.write("Administrador: admin_user / admin1234")
        self.stdout.write("Cliente: demo_user / demo1234")

