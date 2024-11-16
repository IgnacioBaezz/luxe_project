from django.urls import path
from .views import *

urlpatterns = [
    path("", home_bookings, name="home-bookings"),
    path("servicio/<int:pk>", service_detail, name="service-detail"),
    path("reservar/", booking_create, name="booking-create"),
    path("mis-reservas/", booking_list, name="bookings-list")
]