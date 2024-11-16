from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(max_length=300, verbose_name="Descripcion")
    duration = models.DurationField(verbose_name="Duracion")
    price = models.IntegerField(verbose_name="Precio")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta():
        verbose_name = "Servicio"
        verbose_name_plural  = "Servicios"

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Cliente")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Servicio")
    date = models.DateField(verbose_name="Fecha")
    time = models.TimeField(verbose_name="Hora")
    notes = models.CharField(verbose_name="Comentarios", max_length=300)
    active = models.BooleanField(default=False, verbose_name="Activo")
    confirmed = models.BooleanField(default=False, verbose_name="Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta():
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"Reserva de {self.user.username} - {self.service.name} el {self.date} a las {self.time}"
