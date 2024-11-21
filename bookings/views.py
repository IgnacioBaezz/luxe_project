from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service, Booking, BookingStatus
from users.models import Employee
from .forms import BookingForm
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime, timedelta



def root(request):
    return redirect(home_bookings)


def home_bookings(request):
    context = {
        "title":"Reservas | Luxe Therapy",
    }
    return render(request, "bookings/booking_home.html", context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    context = {
        "title":f" {service.name} | Luxe Therapy"
    }
    return render(request, "bookings/service_detail.html", context)

def services_list(request):
    services = Service.objects.filter(active=True)
    context = {
        "title":"Servicios | Luxe Therapy",
        "services":services
    }
    return render(request, "bookings/services_list.html", context)

@login_required
def booking_create(request):
    # Verificar si el usuario es cliente
    if request.user.is_client:
        # Verificar si el usuario ya tiene una reserva pendiente o confirmada
        existing_booking = Booking.objects.filter(
            user=request.user, status__in=[BookingStatus.CONFIRMED, BookingStatus.PENDING]
        ).exists()

        if existing_booking:
            if not (request.user.is_employee or request.user.is_staff):
                return render(request, "bookings/booking_create.html", {
                    "message": "Ya tienes una reserva pendiente o confirmada. Estamos esperando con ansias tu visita."
            })

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

    available_times = [
        ("10:00", "10:00"),
        ("11:00", "11:00"),
        ("12:00", "12:00"),
        ("13:00", "13:00"),
        ("14:00", "14:00"),
        ("15:00", "15:00"),
        ("16:00", "16:00"),
        ("17:00", "17:00"),
        ("18:00", "18:00"),
    ]
    form.fields["time"].choices = available_times

    return render(request, "bookings/booking_create.html", {"form": form})

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def booking_list(request):
    if request.user.is_staff:
        bookings = Booking.objects.filter(active=True).order_by("-created_at")
    else:
        bookings = Booking.objects.filter(user=request.user).order_by("-created_at")

    paginator = Paginator(bookings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "Lista de Reservas | Luxe Therapy",
        "bookings": page_obj,
    }
    return render(request, "bookings/booking_list.html", context)

@login_required
def change_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user.is_staff or booking.user == request.user:
        if action == "confirm":
            booking.status = BookingStatus.CONFIRMED
        elif action == "finalize":
            booking.status = BookingStatus.FINALIZED
            booking.active = False
        elif action == "cancel":
            booking.status = BookingStatus.CANCELLED
            booking.active = False
        booking.save()
    return redirect(booking_list)

@login_required
def booking_detail(request, pk):
    booking = Booking.objects.filter(pk=pk)
    context = {
        "title":f"Detalle reserva | Luxe Therapy",
        "booking":booking
    }
    return render(request, "bookings/booking_detail.html", context)

@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    context = {
        "title":f" Reserva N°{booking.id} | Luxe Therapy",
        "booking":booking
    }
    return render(request, "bookings/booking_edit.html", context)


def get_available_times(request):
    date_str = request.GET.get("date")
    service_id = request.GET.get("service_id")

    if not date_str or not service_id:
        return JsonResponse({"error": "Fecha y servicio son requeridos"}, status=400)

    # Parsear la fecha
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Obtener la hora y fecha actual en el servidor
    now = datetime.now()

    # Verificar si la fecha seleccionada es anterior a la fecha actual
    if date_obj <= now.date():
        return JsonResponse({
            "available_times": [],
            "message": "No hay horas disponibles"
        })

    # Obtener el servicio y su duración
    service = get_object_or_404(Service, id=service_id)
    service_duration = service.duration

    # Configurar las horas de apertura y cierre
    opening_time = datetime.strptime("10:00", "%H:%M").time()
    closing_time = datetime.strptime("19:00", "%H:%M").time()

    # Crear una lista de horarios disponibles en intervalos basados en la duración del servicio
    available_times = []
    current_time = datetime.combine(date_obj, opening_time)

    while current_time.time() <= closing_time:
        end_time = (current_time + service_duration).time()
        if end_time <= closing_time:
            available_times.append(current_time.time().strftime("%H:%M"))
        current_time += service_duration

    # Filtrar las reservas ya hechas para esa fecha y servicio
    bookings = Booking.objects.filter(date=date_obj)
    reserved_times = [booking.time.strftime("%H:%M") for booking in bookings]

    final_times = []

    # Iterar sobre cada horario y verificar la disponibilidad de los empleados
    for time in available_times:
        time_obj = datetime.strptime(time, "%H:%M")
        end_time_obj = time_obj + service_duration

        # Obtener empleados que tienen disponibilidad para ese horario
        day_of_week = date_obj.weekday()
        available_employees = Employee.objects.filter(
            is_available=True,
            availability__day_of_week=day_of_week,
            availability__start_time__lte=time_obj.time(),
            availability__end_time__gte=end_time_obj.time()
        ).distinct()

        # Contar cuántos empleados están disponibles y cuántas reservas ya hay
        if available_employees.exists():
            reservations_at_time = bookings.filter(time=time_obj.time()).count()
            if reservations_at_time < available_employees.count():
                final_times.append(time)

    # Si no hay horarios disponibles, mostrar el mensaje "No hay horas disponibles"
    if not final_times:
        return JsonResponse({
            "available_times": [],
            "message": "No hay horas disponibles"
        })

    return JsonResponse({
        "available_times": final_times,
        "reserved_times": reserved_times
    })
