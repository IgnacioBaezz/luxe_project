from django import forms
from .models import Booking, Service
from datetime import datetime

class BookingForm(forms.ModelForm):
    # Horarios en intervalos de media hora, desde las 10:00 AM hasta las 7:00 PM
    TIME_CHOICES = [
        ("10:00", "10:00 AM"),
        ("10:30", "10:30 AM"),
        ("11:00", "11:00 AM"),
        ("11:30", "11:30 AM"),
        ("12:00", "12:00 PM"),
        ("12:30", "12:30 PM"),
        ("13:00", "1:00 PM"),
        ("13:30", "1:30 PM"),
        ("14:00", "2:00 PM"),
        ("14:30", "2:30 PM"),
        ("15:00", "3:00 PM"),
        ("15:30", "3:30 PM"),
        ("16:00", "4:00 PM"),
        ("16:30", "4:30 PM"),
        ("17:00", "5:00 PM"),
        ("17:30", "5:30 PM"),
        ("18:00", "6:00 PM"),
    ]

    time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = Booking
        exclude = ["user"]
        fields = ["service", "date", "time", "notes", "user"]
        labels = {
            "service": "Servicio",
            "date": "Fecha",
            "time": "Hora",
            "notes": "Comentarios adicionales",
        }
        widgets = {
            "service": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),  # Selector de fecha estilizado
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay una fecha seleccionada, filtrar las horas ya reservadas para esa fecha
        if self.instance.date:
            self.filter_reserved_times(self.instance.date)

    def filter_reserved_times(self, date):
        # Filtrar las reservas existentes para la fecha seleccionada
        booked_times = Booking.objects.filter(date=date).values_list('time', flat=True)

        # Actualizar las opciones de hora, eliminando las ya reservadas
        available_times = [
            time for time, label in self.TIME_CHOICES if time not in booked_times
        ]

        # Actualizar el campo de horas en el formulario con las horas disponibles
        self.fields['time'].choices = [(time, label) for time, label in self.TIME_CHOICES if time in available_times]
