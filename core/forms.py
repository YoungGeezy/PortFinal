from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Colegio, Nota, Observacion, User, Contacto, Asistencia

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
#Clase para el formulario
class ContactoForm(forms.ModelForm):
    class Meta:
        model=Contacto
        fields = '__all__'


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        
        fields = '__all__'

class ObservacionForm(forms.ModelForm):
    class Meta:
        model = Observacion       
        fields = '__all__'

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia       
        fields = '__all__'

class ColegioForm(forms.ModelForm):
    class Meta:
        model = Colegio       
        fields = '__all__'