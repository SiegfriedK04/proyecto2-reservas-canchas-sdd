import json
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .forms import RegistrationForm
from .models import Booking, Court
from .services import available_slots, can_cancel_booking, cancel_booking, create_booking, nearest_alternatives


class CourtLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class CourtLogoutView(LogoutView):
    next_page = reverse_lazy("reservations:home")


def home(request):
    courts = Court.objects.filter(is_active=True)
    return render(request, "reservations/home.html", {"courts": courts})


def register(request):
    if request.user.is_authenticated:
        return redirect("reservations:home")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Tu cuenta está lista. Ya puedes reservar una cancha.")
        return redirect("reservations:home")
    return render(request, "registration/register.html", {"form": form})


@ensure_csrf_cookie
def booking_calendar(request, court_id):
    court = get_object_or_404(Court, pk=court_id, is_active=True)
    initial_day = max(timezone.localdate() + timedelta(days=1), timezone.localdate())
    return render(
        request,
        "reservations/calendar.html",
        {"court": court, "initial_date": initial_day.isoformat()},
    )


@require_GET
def availability_api(request, court_id):
    court = get_object_or_404(Court, pk=court_id, is_active=True)
    try:
        day = date.fromisoformat(request.GET.get("date", ""))
    except ValueError:
        return JsonResponse({"error": "La fecha debe usar el formato AAAA-MM-DD."}, status=400)

    return JsonResponse(
        {
            "court": {"id": court.pk, "name": court.name, "slot_minutes": court.slot_minutes},
            "date": day.isoformat(),
            "slots": available_slots(court=court, day=day),
        }
    )


def _aware_datetime(value):
    parsed = parse_datetime(value or "")
    if parsed is None:
        raise ValueError("Fecha u hora inválida.")
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


@require_POST
def create_booking_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Debes iniciar sesión para reservar.", "code": "authentication_required"}, status=403)
    try:
        payload = json.loads(request.body or "{}")
        court = Court.objects.get(pk=payload.get("court_id"), is_active=True)
        starts_at = _aware_datetime(payload.get("starts_at"))
        ends_at = _aware_datetime(payload.get("ends_at"))
        booking = create_booking(
            user=request.user,
            court=court,
            starts_at=starts_at,
            ends_at=ends_at,
        )
    except (json.JSONDecodeError, ValueError, Court.DoesNotExist):
        return JsonResponse({"error": "La solicitud de reserva no es válida.", "code": "invalid_request"}, status=400)
    except ValidationError as error:
        alternatives = nearest_alternatives(court=court, starts_at=starts_at, ends_at=ends_at)
        if hasattr(error, "message_dict"):
            message = next(iter(error.message_dict.values()))[0]
        else:
            message = error.messages[0]
        return JsonResponse(
            {
                "error": message,
                "code": "booking_rejected",
                "alternatives": alternatives,
            },
            status=409,
        )

    return JsonResponse(
        {
            "success": True,
            "booking": {
                "id": booking.pk,
                "court": booking.court.name,
                "starts_at": booking.starts_at.isoformat(),
                "ends_at": booking.ends_at.isoformat(),
            },
        },
        status=201,
    )


@login_required
def my_bookings(request):
    bookings = list(request.user.court_bookings.select_related("court").all())
    for booking in bookings:
        booking.can_cancel = can_cancel_booking(booking=booking, actor=request.user)
    return render(request, "reservations/my_bookings.html", {"bookings": bookings})


@require_POST
@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    try:
        cancel_booking(booking=booking, actor=request.user)
    except ValidationError as error:
        messages.error(request, error.messages[0])
    else:
        messages.success(request, "La reserva fue cancelada y el horario volvió a estar disponible.")
    return redirect("reservations:my_bookings")

