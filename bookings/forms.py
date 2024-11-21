from django import forms
from .models import Booking, Service
from django.utils import timezone
from datetime import datetime

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ["user"]
        fields = ["service", "date", "time", "notes"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-select", "placeholder": "Selecciona un servicio"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "service": "Servicio",
            "date": "Fecha",
            "time": "Hora",
            "notes": "Comentario (opcional)",
        }

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        empty_label="Selecciona un servicio",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date and time:
            selected_datetime = timezone.make_aware(datetime.combine(date, time))
            if selected_datetime <= timezone.now():
                raise forms.ValidationError("La fecha y hora seleccionadas deben estar en el futuro.")