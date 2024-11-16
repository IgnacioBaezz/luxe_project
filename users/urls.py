from django.urls import path
from .views import *


urlpatterns = [
    path("registro/", register_user, name="register"),
    path("iniciar-sesion/", login_user, name="login"),
    path("cerrar-sesion", logout_user, name="logout"),
    path("perfil/", profile_user, name="profile"),
    path("editar-perfil", profile_edit, name="profile-edit"),
]
