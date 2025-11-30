from django.db import models
from django.contrib.auth.models import User
#from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field

# ACTIVIDAD Y COMPONENTES (componentes van en actividades)
class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo



from formulario.models import Formulario

class Componente(models.Model):
    TIPOS = (
        ("texto", "Texto"),
        ("foro", "Foro"),
        ("examen", "Examen"),
        ("cuestionario", "Cuestionario"),
        ("recurso", "Recurso"),
    )
    actividad = models.ForeignKey(Actividad, related_name="componentes", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    contenido = models.TextField(blank=True)
    formulario = models.ForeignKey(Formulario, null=True, blank=True, on_delete=models.SET_NULL, related_name="componentes")

    def __str__(self):
        return f"{self.tipo} - {self.actividad.titulo}"


# FORO
class Foro(models.Model):
    componente = models.OneToOneField(Componente, on_delete=models.CASCADE, related_name="foro")
    titulo = models.CharField(max_length=255)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo


# COMENTARIOS DENTRO DE FORO
class Comentario(models.Model):
    foro = models.ForeignKey(Foro, related_name="comentarios", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username}"


# EXAMEN
class Examen(models.Model):
    componente = models.OneToOneField(Componente, on_delete=models.CASCADE, related_name="examen")
    titulo = models.CharField(max_length=255)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo


# CUESTIONARIO
class Cuestionario(models.Model):
    componente = models.OneToOneField(Componente, on_delete=models.CASCADE, related_name="cuestionario")
    titulo = models.CharField(max_length=255)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo
    
@receiver(post_save, sender=Componente)
def crear_foro_automatico(sender, instance, created, **kwargs):
    if created and instance.tipo == "foro":
        Foro.objects.create(
            componente=instance,
            titulo=instance.contenido or "Foro",
            descripcion=""
        )

@receiver(post_save, sender=Componente)
def crear_examen_automatico(sender, instance, created, **kwargs):
    if created and instance.tipo == "examen":
        Examen.objects.create(
            componente=instance,
            titulo=instance.contenido or "Examen",
            descripcion=""
        )

@receiver(post_save, sender=Componente)
def crear_cuestionario_automatico(sender, instance, created, **kwargs):
    if created and instance.tipo == "cuestionario":
        Cuestionario.objects.create(
            componente=instance,
            titulo=instance.contenido or "Cuestionario",
            descripcion=""
        )
