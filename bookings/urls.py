from django.urls import path
from .views import *

urlpatterns = [
    path("", root),
    path("inicio", home_bookings, name="home-bookings"),
    # path("servicio/<int:pk>", service_detail, name="service-detail"),
    path("reserva/<int:pk>",booking_detail, name="booking-detail"),
    path("reservar/", booking_create, name="booking-create"),
    path("mis-reservas/", booking_list, name="bookings-list"),
    path("servicios/", services_list, name="services-list"),
    path("get-available-times/", get_available_times, name="get_available_times"),
    path("booking/<int:booking_id>/<str:action>/", change_booking_status, name="change-booking-status"),
]