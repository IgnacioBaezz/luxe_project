from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service, Booking
from .forms import BookingForm
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages

def root(request):
    return redirect(booking_list)


def home_bookings(request):
    services = Service.objects.all()
    context = {
        "title":"Reservas | Luxe Therapy",
        "services":services
    }
    return render(request, "bookings/booking_home.html", context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    context = {
        "title":f" {service.name} | Luxe Therapy"
    }
    return render(request, "bookings/service_detail.html", context)

@login_required
def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Reserva realizada con éxito.")
            return redirect(booking_list)
    else:
        form = BookingForm()

    return render(request, "bookings/booking_create.html", {"form": form})


@login_required
def booking_list(request):
    if request.user.is_staff:
        bookings = Booking.objects.filter(active=True)
    else:
        bookings = Booking.objects.filter(usuario=request.user, active=True)
    context = {
        "title":"Lista de Reservas | Luxe Therapy",
        "bookings":bookings
    }
    return render(request, "bookings/booking_list.html", context)

@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    context = {
        "title":f" Reserva N°{booking.id} | Luxe Therapy",
        "booking":booking
    }
    return render(request, "bookings/booking_edit.html", context)

def get_available_times_ajax(request):
    date_str = request.GET.get("date")
    service_id = request.GET.get("service_id")
    
    if date_str and service_id:
        try:
            # Convierte la fecha a formato adecuado
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            service = Service.objects.get(id=service_id)
            
            # Obtener las reservas para esa fecha y servicio
            bookings = Booking.objects.filter(service_id=service_id, date=date)
            
            # Extraer las horas reservadas
            reserved_times = [booking.time.strftime("%H:%M") for booking in bookings]

            # Definir las horas disponibles (ajustar a tu lógica de negocio)
            available_times = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
            
            # Devuelve las horas disponibles y reservadas
            return JsonResponse({
                "available_times": available_times,
                "reserved_times": reserved_times
            })
        
        except Service.DoesNotExist:
            return JsonResponse({"error": "Servicio no encontrado."}, status=404)
    
    return JsonResponse({"error": "Parámetros inválidos."}, status=400)

def get_available_times(request):
    date_str = request.GET.get("date")
    service_id = request.GET.get("service_id")
    
    # Filtrar las reservas para esa fecha y servicio
    bookings = Booking.objects.filter(service_id=service_id, date=date_str)

    # Extraer las horas reservadas
    reserved_times = [booking.time.strftime("%H:%M") for booking in bookings]

    # Horas disponibles (esto dependerá de tus datos o lógica de negocio)
    available_times = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

    return JsonResponse({
        "available_times": available_times,
        "reserved_times": reserved_times
    })

