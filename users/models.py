from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name="Numero de telefono")
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
        return f"{self.user.username}"

class EmployeeAvailability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="availability")
    day_of_week = models.IntegerField(choices=[
        (0, "Lunes"), (1, "Martes"), (2, "Miércoles"),
        (3, "Jueves"), (4, "Viernes"), (5, "Sábado"), (6, "Domingo")
    ])
    start_time = models.TimeField(verbose_name="Hora de inicio")
    end_time = models.TimeField(verbose_name="Hora de fin")

    class Meta:
        verbose_name = "Disponibilidad del Empleado"
        verbose_name_plural = "Disponibilidad de Empleados"

    def __str__(self):
        return f"{self.employee.user.username} disponibilidad {self.get_day_of_week_display()}"
    