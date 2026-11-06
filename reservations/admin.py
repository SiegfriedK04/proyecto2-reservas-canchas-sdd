from django.contrib import admin

from .models import AuditEvent, Booking, Court, CourtBlock


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "opening_time", "closing_time", "slot_minutes", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("court", "user", "starts_at", "ends_at", "status")
    list_filter = ("status", "court")
    search_fields = ("court__name", "user__username", "user__email")


@admin.register(CourtBlock)
class CourtBlockAdmin(admin.ModelAdmin):
    list_display = ("court", "starts_at", "ends_at", "reason", "created_by")
    list_filter = ("court",)


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "entity_type", "entity_id", "actor", "created_at")
    list_filter = ("event_type", "entity_type")
    readonly_fields = ("actor", "event_type", "entity_type", "entity_id", "details", "created_at")

