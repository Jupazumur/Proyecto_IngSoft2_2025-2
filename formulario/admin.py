
from django.contrib import admin
from .models import Pregunta, Opcion, Respuesta, Formulario
@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
	list_display = ("nombre", "descripcion")

class OpcionInline(admin.TabularInline):
	model = Opcion
	extra = 1

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
	list_display = ("texto", "tipo")
	inlines = [OpcionInline]

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
	list_display = ("texto", "pregunta")

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
	list_display = ("pregunta", "opcion", "texto", "usuario", "fecha")

# Register your models here.
