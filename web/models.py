from django.db.models import Model, EmailField, CharField, TextField, FileField, BooleanField, DateField

class Article(Model):
    img = FileField(null=True, blank=True, verbose_name="Imagen")
    title = CharField(max_length=30, verbose_name="Titulo")
    content = CharField(max_length=300, verbose_name="Contenido")
    active = BooleanField(default=False, verbose_name="Activo")
    created_at = DateField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated_at = DateField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta():
        verbose_name = "Article"
        verbose_name_plural = "Articulos"

