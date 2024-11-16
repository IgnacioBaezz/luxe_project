from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, TextInput, Textarea, EmailInput, DateInput
from .models import User



class UserRegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = ["username","email", "password1", "password2"]
        widgets = {
            "username":TextInput(attrs={"class":"form-control","id":"id_username","placeholder":"Nombre de usuario"}),
            "email":EmailInput(attrs={"class":"form-control","type":"email","id":"id_email","placeholder":"Correo electronico","data-bs-theme":"dark"}),
        }
        labels = {
            "username":"Nombre de usuario",
            "email":"Correo electronico",
            "password1":"Contraseña",
            "password2":"Contraseña (confirmacion)"
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget = TextInput(attrs={"class": "form-control", "type": "password", "placeholder": "Contraseña"})
        self.fields["password2"].widget = TextInput(attrs={"class": "form-control", "type": "password", "placeholder": "Contraseña (confirmación)"})

class UserLoginForm(AuthenticationForm):
    class Meta():
        model = User
        fields = ["username","password"]
        labels = {
            "username":"Nombre de usuario",
            "password":"Contraseña"
        }

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"})
        self.fields["password"].widget = TextInput(attrs={"class": "form-control", "type": "password", "placeholder": "Contraseña"})    


class UserProfileForm(ModelForm):
    class Meta():
        model = User
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "email":EmailInput(attrs={"class":"form-control","type":"email","placeholder":"Correo electronico","disabled":True}),
            "first_name":TextInput(attrs={"class":"form-control","placeholder":"Nombre","type":"text","aria-label":"Nombre","disabled":True}),
            "last_name":TextInput(attrs={"class":"form-control","placeholder":"Apellido","type":"text","aria-label":"Apellido","disabled":True}),
        }