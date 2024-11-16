from django.shortcuts import render
from django.conf.urls import handler404


def maintenance(request):
    context = {
        "title":"Mantenimiento | Luxe Therapy"
    }
    return render(request, "core/maintenance.html")

def custom_page_not_found_view(request, exception):
    return render(request, "core/404.html", status=404)

handler404 = custom_page_not_found_view