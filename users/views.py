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

# Vista basada en función

@login_not_required
def register_user(request):
    user_type = request.GET.get("user_type", None)
    context = {"user_type":user_type}
    if user_type is not None:
        if context["user_type"] == "member": 
            message1 = "Únete a nuestro grupo de socios"
            message2 = "Gestiona tus propiedades"
            title = "Registro Socio | Inmobilaria Báez"
        elif context["user_type"] == "customer":
            message1 = "Hazte cliente"
            message2 = "Obtén beneficios exclusivos y promociones"
            title = "Registro Cliente | Inmobilaria Báez"
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        context["form"] = form
        if form.is_valid():
            user = form.save()
            if user_type == "member":
                asign_group_member(user)
            elif user_type == "customer":
                asign_group_customer(user)
            else:
                return redirect('error_page') # No implementado
            context["form"] = form
            login(request, user)
            return redirect(index)
    else:
        context["form"] = UserRegisterForm

    context.update({
                "title":title,
                "message1":message1,
                "message2":message2,
            })
    return render(request, "users/register.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect(index)

@login_not_required
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
        user = User.objects.get(username=username)
        user.password == request.POST["password"]
        # user = authenticate(request,username=request.POST["username"],password=request.POST["password"])
        if user == None:
            return render(request, "web/index.html", context)
        else:
            login(request, user)
            return redirect(index)

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