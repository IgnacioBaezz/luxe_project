from django.db import models

class EmailNotification(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, verbose_name="Asunto")
    message = models.TextField(verbose_name="Mensaje")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado a")

    class Meta():
        verbose_name = "Notificacion de email"
        verbose_name_plural = "Notificaciones de email"

    def __str__(self):
        return f"Correo enviado a {self.user.get_complete_name} | {self.sent_at}"