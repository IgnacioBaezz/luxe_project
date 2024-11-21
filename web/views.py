from django.shortcuts import render, redirect
from .models import Article

def root(request):
    return redirect(index)

def index(request):
    context = {
        "title":"Inicio | Luxe Theraphy"
    }
    return render(request, "web/index.html", context)

def about(request):
    context = {
        "title":"Sobre nosotros | Luxe Therapy"
    }
    return render(request, "web/about.html", context)