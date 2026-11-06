from django.urls import path

from . import views


app_name = "reservations"
urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.register, name="register"),
    path("login/", views.CourtLoginView.as_view(), name="login"),
    path("logout/", views.CourtLogoutView.as_view(), name="logout"),
    path("canchas/<int:court_id>/reservar/", views.booking_calendar, name="booking_calendar"),
    path("mis-reservas/", views.my_bookings, name="my_bookings"),
    path("mis-reservas/<int:booking_id>/cancelar/", views.cancel_booking_view, name="cancel_booking"),
    path("api/canchas/<int:court_id>/disponibilidad/", views.availability_api, name="availability_api"),
    path("api/reservas/", views.create_booking_api, name="create_booking_api"),
]

