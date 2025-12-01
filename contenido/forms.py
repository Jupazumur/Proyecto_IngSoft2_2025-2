from django import forms
from .models import Actividad, Componente


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["titulo", "descripcion"]


class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        fields = ["tipo", "titulo", "formulario"]
