from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Court(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=160, blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    slot_minutes = models.PositiveSmallIntegerField(default=60)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def clean(self):
        if self.opening_time and self.closing_time and self.closing_time <= self.opening_time:
            raise ValidationError({"closing_time": "La hora de cierre debe ser posterior a la apertura."})
        if self.slot_minutes not in {30, 45, 60, 90, 120}:
            raise ValidationError({"slot_minutes": "La duración debe ser de 30, 45, 60, 90 o 120 minutos."})

    def __str__(self):
        return self.name


class CourtBlock(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="blocks")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    reason = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="court_blocks_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("starts_at",)
        indexes = [models.Index(fields=("court", "starts_at", "ends_at"))]

    def clean(self):
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValidationError({"ends_at": "El final del bloqueo debe ser posterior al inicio."})

    def __str__(self):
        return f"{self.court} - {self.reason}"


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmada"
        CANCELLED = "cancelled", "Cancelada"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="court_bookings")
    court = models.ForeignKey(Court, on_delete=models.PROTECT, related_name="bookings")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-starts_at",)
        indexes = [
            models.Index(fields=("court", "starts_at", "ends_at", "status")),
            models.Index(fields=("user", "starts_at")),
        ]

    def clean(self):
        errors = {}
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            errors["ends_at"] = "La hora final debe ser posterior a la hora inicial."
        if self.starts_at and self.status == self.Status.CONFIRMED and self.starts_at <= timezone.now():
            errors["starts_at"] = "No se puede reservar un horario pasado."

        if self.court_id and self.starts_at and self.ends_at and not errors:
            local_start = timezone.localtime(self.starts_at)
            local_end = timezone.localtime(self.ends_at)
            if local_start.date() != local_end.date():
                errors["ends_at"] = "La reserva debe comenzar y terminar el mismo día."
            elif local_start.time() < self.court.opening_time or local_end.time() > self.court.closing_time:
                errors["starts_at"] = "El horario está fuera de la operación de la cancha."

            booking_conflicts = Booking.objects.filter(
                court=self.court,
                status=self.Status.CONFIRMED,
                starts_at__lt=self.ends_at,
                ends_at__gt=self.starts_at,
            ).exclude(pk=self.pk)
            block_conflicts = CourtBlock.objects.filter(
                court=self.court,
                starts_at__lt=self.ends_at,
                ends_at__gt=self.starts_at,
            )
            if booking_conflicts.exists():
                errors["starts_at"] = "El horario seleccionado ya está reservado."
            elif block_conflicts.exists():
                errors["starts_at"] = "La cancha está bloqueada durante ese horario."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.court} - {self.user} - {self.starts_at:%Y-%m-%d %H:%M}"


class AuditEvent(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservation_audit_events",
    )
    event_type = models.CharField(max_length=40)
    entity_type = models.CharField(max_length=40)
    entity_id = models.PositiveBigIntegerField()
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("entity_type", "entity_id", "created_at"))]

    def __str__(self):
        return f"{self.event_type} {self.entity_type}#{self.entity_id}"

