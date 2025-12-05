from django.db import models
from django.contrib.auth.models import User
from contenido.models import Componente

class Intento(models.Model):
    """
    Modelo que representa un intento de un usuario para responder un examen o cuestionario.
    Agrupa todas las respuestas de un usuario en una sola sesión.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="intentos")
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name="intentos")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Intento"
        verbose_name_plural = "Intentos"
    
    def __str__(self):
        tipo = self.componente.tipo
        return f"Intento de {self.usuario.username} - {tipo.capitalize()}: {self.componente.titulo} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"