from django.urls import path
from .views import * 

urlpatterns = [
    path("", root),
    path("inicio/", index, name="index"),
    path("eventos/", events, name="events"),
    path("sobre-nosotros/", about, name="about")
]
