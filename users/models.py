from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_employee = models.BooleanField(default=False, verbose_name="Es empleado")
    is_client = models.BooleanField(default=True, verbose_name="Es cliente")

    class Meta():
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username}"
       
    def get_complete_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.ManyToManyField("bookings.Service", verbose_name="Especialidad")
    is_available = models.BooleanField(default=True, verbose_name="Está disponible")

    class Meta():
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return self.user.get_full_name()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Numero de Telefono")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Direccion")
    preferences = models.JSONField(blank=True, null=True, verbose_name="Preferencias")

    class Meta():
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"

    def __str__(self):
        return self.user.username
    
    