from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy as _
from django.contrib import messages

from .services import asign_group_member, asign_group_customer
from .forms import UserRegisterForm, UserProfileForm, UserLoginForm
from .models import User
from time import sleep
from bookings.views import *
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import UserRegisterForm, UserLoginForm

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home-bookings")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home-bookings")

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home-bookings")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home-bookings")
        

@login_required
def profile_user(request, pk):
    u = get_object_or_404(User, pk=pk)

    user_keys = ["Nombre de usuario","Correo electronico","Numero de Telefono"]
    user_list = [u.username,u.email,u.phone_number]
    user_info = {}
    i = 0
    for x in user_list:
        if x:
            user_info.update({user_keys[i]:x})
        else:
            user_info.update({user_keys[i]:None})
        i += 1

    context = {
        "title": f"Perfil {u.username} | Luxe Therapy",
        "usuario_info": user_info,
        "u":u
    }
    return render(request, "users/profile.html", context)