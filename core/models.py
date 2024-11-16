from django.db.models import Model, EmailField, CharField, TextField, DateField, DateTimeField

class ContactModel(Model):
    customer_email = EmailField(verbose_name="Correo Cliente")
    customer_name = CharField(max_length=64)
    message = TextField(verbose_name="Mensaje")
    created_at = DateField(auto_now_add=True,verbose_name="Fecha de creacion")
    updated_at = DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta():
        verbose_name = "Formulario de Contacto"
        verbose_name_plural = "Formularios de Contacto"