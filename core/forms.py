from django.forms import ModelForm, TextInput, EmailInput, Textarea
from .models import ContactForm

class ContactFormModelForm(ModelForm):
    class Meta():
        model = ContactForm

        fields = ["customer_name","customer_email","message"]

        widgets = {
            "customer_name":TextInput(attrs={"class":"form-control mb-3","placeholder":"Nombre Apellido"}),
            "customer_email":EmailInput(attrs={"class":"form-control mb-3","type":"email","placeholder":"Ejemplo@correo.cl"}),
            "message":Textarea(attrs={"class":"form-control mb-3","rows":"3","placeholder":"Deja un mensaje adicional para nosotros!!!"})
        }
        labels = {
            "customer_name":"Nombre",
            "customer_email":"Correo Electronico",
            "message":"Mensaje"
        }