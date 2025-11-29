
from django.db import models

class Formulario(models.Model):
	nombre = models.CharField(max_length=255)
	descripcion = models.TextField(blank=True)

	def __str__(self):
		return self.nombre

class Pregunta(models.Model):
	TIPO_PREGUNTA = [
		('abierta', 'Abierta'),
		('opcion_multiple', 'Opción múltiple'),
	]

	formulario = models.ForeignKey(Formulario, related_name='preguntas', on_delete=models.CASCADE)
	texto = models.CharField(max_length=255)
	tipo = models.CharField(max_length=20, choices=TIPO_PREGUNTA)

	def __str__(self):
		return self.texto

class Opcion(models.Model):
	pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
	texto = models.CharField(max_length=255)
	correcta = models.BooleanField(default=False)

	def __str__(self):
		return self.texto

class Respuesta(models.Model):
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	opcion = models.ForeignKey(Opcion, null=True, blank=True, on_delete=models.SET_NULL)
	texto = models.TextField(blank=True)
	usuario = models.CharField(max_length=150, blank=True)  # Opcional: para identificar quién responde
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Respuesta a '{self.pregunta.texto}'"
# Create your models here.
