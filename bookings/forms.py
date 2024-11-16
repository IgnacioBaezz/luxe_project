from django import forms
from .models import Reserva

class BookingForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["servicio", "fecha", "hora", "comentarios"]
        widgets = {
            "servicio":forms.Select(attrs={"class":"select-form"}),
            
        }