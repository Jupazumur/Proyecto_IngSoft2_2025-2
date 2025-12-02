from django import forms
from .models import Actividad, Componente, Foro, Examen, Cuestionario


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["titulo", "descripcion"]


class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        fields = ["tipo", "titulo", "formulario"]


class ForoForm(forms.ModelForm):
    class Meta:
        model = Foro
        fields = ["descripcion"]

class ExamenDescForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ["descripcion"]

class CuestionarioDescForm(forms.ModelForm):
    class Meta:
        model = Cuestionario
        fields = ["descripcion"]
