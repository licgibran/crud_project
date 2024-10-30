from django import forms
from .models import Cliente
##probando login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'pais', 'fecha_nac', 'foto']

        #Sobrescribir el campo 'foto' para asegurarnos de que es un campo de tipo archivo
        foto = forms.ImageField(required=False)  # La imagen es opcional


## probando login
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]