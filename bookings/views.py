from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, Booking
from .forms import BookingForm


def home_bookings(request):
    services = Service.objects.all()
    context = {
        "title":"Reservas | Luxe Therapy",
        "services":services
    }
    return render(request, "bookings/home.html", context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    context = {
        "title":f" {service.name} | Luxe Therapy"
    }
    return render(request, "bookings/service_detail.html", context)

def booking_create(request):
    context = {
        "title":"Agendar Reserva | Luxe Therapy"
    }
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.usuario = request.user
            booking.save()
            return redirect(home_bookings)
    else:
        form = BookingForm()
    context["form"] = form
    return render(request, "reservas_spa/reserva_form.html", context)

def booking_list(request):
    if request.user.is_staff:
        bookings = Booking.objects.filter(active=True)
    else:
        bookings = Booking.objects.filter(usuario=request.user, active=True)
    context = {
        "title":"Lista de Reservas | Luxe Therapy",
        "bookings":bookings
    }
    return render(request, "reservas_spa/reservas_list.html", context)

def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    context = {
        "title":f" Reserva N°{booking.id} | Luxe Therapy",
        "booking":booking
    }
    return render(request, "bookings/booking_edit.html", context)