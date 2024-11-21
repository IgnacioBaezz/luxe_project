from django.urls import path
from .views import *


urlpatterns = [
    path("registro/", UserRegisterView.as_view(), name="register"),
    path("iniciar-sesion/", UserLoginView.as_view(), name="login"),
    path("cerrar-sesion", UserLogoutView.as_view(), name="logout"),
    path("perfil/<int:pk>", profile_user, name="profile"),
]
