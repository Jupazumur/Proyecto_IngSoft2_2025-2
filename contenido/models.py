from django.db import models
from django.contrib.auth.models import User
#from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field

### ACTIVIDAD Y COMPONENTES ###
class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo


from formulario.models import Formulario

# Componentes se encarga de crear y enlazar los modelos de los tipos a una actividad
class Componente(models.Model):
    TIPOS = (
        ("foro", "Foro"),
        ("examen", "Examen"),
        ("cuestionario", "Cuestionario"),
    )
    actividad = models.ForeignKey(Actividad, related_name="componentes", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.TextField(blank=True)
    formulario = models.ForeignKey(Formulario, null=True, blank=True, on_delete=models.SET_NULL, related_name="componentes")

    def __str__(self):
        return f"{self.tipo} - {self.actividad.titulo}"

### FORO Y COMENTARIOS ###
class Foro(models.Model):
    componente = models.OneToOneField(Componente, on_delete=models.CASCADE, related_name="foro")
    titulo = models.CharField(max_length=255)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    foro = models.ForeignKey(Foro, related_name="comentarios", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username}"

### EXAMEN Y CUESTIONARIO ###
## Examen y Cuestionario son practicamente lo mismo, solo que Examen no tiene disponible el bloque

class Examen(models.Model):
    componente = models.OneToOneField(Componente, on_delete=models.CASCADE, related_name="examen")
    titulo = models.CharField(max_length=255)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo

class Cuestionario(models.Model):
    componente = models.OneToOneField(Componente, on_delete=models.CASCADE, related_name="cuestionario")
    titulo = models.CharField(max_length=255)
    descripcion = CKEditor5Field('Text', config_name='extends', blank=True)

    def __str__(self):
        return self.titulo

### CREACION DE MODELOS AUTOMATICOS AL CREAR COMPONENTES ###

# Crear modelo Foro al crear componente tipo Foro
@receiver(post_save, sender=Componente)
def crear_foro_automatico(sender, instance, created, **kwargs):
    if created and instance.tipo == "foro":
        Foro.objects.create(
            componente=instance,
            titulo=instance.titulo or "Foro",
            descripcion=""
        )

# Crear modelo Examen al crear componente tipo Examen
@receiver(post_save, sender=Componente)
def crear_examen_automatico(sender, instance, created, **kwargs):
    if created and instance.tipo == "examen":
        Examen.objects.create(
            componente=instance,
            titulo=instance.titulo or "Examen",
            descripcion=""
        )

# Crear modelo Cuestionario al crear componente tipo Cuestionario
@receiver(post_save, sender=Componente)
def crear_cuestionario_automatico(sender, instance, created, **kwargs):
    if created and instance.tipo == "cuestionario":
        Cuestionario.objects.create(
            componente=instance,
            titulo=instance.titulo or "Cuestionario",
            descripcion=""
        )

# Crear automaticamente Formulario al crear Examen o Cuestionario
@receiver(post_save, sender=Componente)
def crear_formulario_automatico(sender, instance, created, **kwargs):
    if created and instance.tipo in ["examen", "cuestionario"] and not instance.formulario:

        nombre_formulario = f"Formulario de {instance.tipo.capitalize()} - {instance.actividad.titulo}"
        formulario = Formulario.objects.create(
            nombre=nombre_formulario,
            descripcion=f"Formulario asociado al {instance.tipo} de la actividad: {instance.actividad.titulo}"
        )

        Componente.objects.filter(id=instance.id).update(formulario=formulario)

# Sincronizar titulo del componente con el modelo relacionado
@receiver(post_save, sender=Componente)
def sincronizar_titulo_componente(sender, instance, created, **kwargs):
    if not created:  # Solo cuando se actualiza, no cuando se crea
        if instance.tipo == "foro" and hasattr(instance, 'foro'):
            if instance.foro.titulo != instance.titulo:
                instance.foro.titulo = instance.titulo
                instance.foro.save(update_fields=['titulo'])
        elif instance.tipo == "examen" and hasattr(instance, 'examen'):
            if instance.examen.titulo != instance.titulo:
                instance.examen.titulo = instance.titulo
                instance.examen.save(update_fields=['titulo'])
        elif instance.tipo == "cuestionario" and hasattr(instance, 'cuestionario'):
            if instance.cuestionario.titulo != instance.titulo:
                instance.cuestionario.titulo = instance.titulo
                instance.cuestionario.save(update_fields=['titulo'])