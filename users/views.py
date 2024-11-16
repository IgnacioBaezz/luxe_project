from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy as _
from django.contrib import messages

from .services import asign_group_member, asign_group_customer
from .forms import UserRegisterForm, UserProfileForm, UserLoginForm
from web.views import *
from .models import User
from time import sleep
from bookings.views import *

# Vista basada en función

@login_not_required
def register_user(request):
    context = {}
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        context["form"] = form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(home_bookings)
    else:
        context["form"] = UserRegisterForm
    return render(request, "users/register.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect(home_bookings)

def login_user(request):
    context = {
        "form":UserLoginForm,
        "title":"Login",
        "error":"El usuario o contraseña son incorrectos"
    }
    if request.method == "GET":
        return render(request, "users/login.html", context)
    else:
        username = request.POST["username"]
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        
        # user = authenticate(request,username=request.POST["username"],password=request.POST["password"])
        if user == None:
            return redirect(login_user)
        else:
            if user.password == request.POST["password"]:
                login(request, user)
                return redirect(home_bookings)
            else: redirect(login_user)
        

@login_required
def profile_user(request):
    if request.user.is_authenticated:
        u = request.user
        user_groups = request.user.groups.all()
        user_keys = ["Nombre de usuario", "Nombre", "Apellido", "Correo electronico","Descripcion"]
        user_list = [u.username,u.first_name,u.last_name,u.email,u.description]
        user_info = {}
        i = 0
        for x in user_list:
            if x:
                user_info.update({user_keys[i]:x})
            else:
                user_info.update({user_keys[i]:None})
            i += 1

        context = {
            "title": f"Perfil {u.username} | Báez Inmobiliaria",
            "usuario_info": user_info,
            "user_groups":user_groups,
        }
        return render(request, "users/profile.html", context)
    else:
        return redirect(login_user)


@login_required
def profile_edit(request):
    usuario = request.user
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=usuario)
        
        if form.is_valid():
            print(form.cleaned_data)
            if form.has_changed():
                form.save()
                messages.success(request, "Tu perfil ha sido actualizado exitosamente.")
                return redirect(profile_user)
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=usuario)

    context = {
        "title": "Editar Perfil | Báez Inmobiliaria",
        "form": form,
        "user": usuario
    }
    return render(request, "users/profile_edit.html", context)