from django.shortcuts import render, get_object_or_404, redirect
from .models import Actividad, Foro, Comentario, Componente, Examen
from formulario.models import Formulario
from .forms import ActividadForm, ComponenteForm
def examen_detalle(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id, tipo="examen")
    examen = get_object_or_404(Examen, componente=componente)
    formulario = componente.formulario
    preguntas = formulario.preguntas.prefetch_related('opciones').all() if formulario else []
    mensaje = None

    if request.method == "POST":
        if not request.user.is_authenticated:
            mensaje = "Debes iniciar sesión para responder el examen."
        else:
            from formulario.models import Respuesta, Opcion
            for pregunta in preguntas:
                key = f"pregunta_{pregunta.id}"
                valor = request.POST.get(key)
                if pregunta.tipo == 'abierta':
                    if valor:
                        Respuesta.objects.create(
                            pregunta=pregunta,
                            texto=valor,
                            usuario=request.user.username
                        )
                elif pregunta.tipo == 'opcion_multiple':
                    if valor:
                        opcion = Opcion.objects.filter(id=valor, pregunta=pregunta).first()
                        Respuesta.objects.create(
                            pregunta=pregunta,
                            opcion=opcion,
                            usuario=request.user.username
                        )
            mensaje = "Respuestas enviadas correctamente."

    return render(request, "contenido/examen_detalle.html", {
        "componente": componente,
        "examen": examen,
        "formulario": formulario,
        "preguntas": preguntas,
        "mensaje": mensaje,
    })
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def teaching_sequence(request):
    actividades = Actividad.objects.prefetch_related("componentes").all()
    return render(request, "contenido/secuencia.html", {"activities": actividades})


def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teaching_sequence')
    else:
        form = ActividadForm()
    return render(request, 'contenido/actividad_form.html', {'form': form})


def agregar_componente(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if request.method == 'POST':
        form = ComponenteForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.actividad = actividad
            comp.save()
            return redirect('teaching_sequence')
    else:
        form = ComponenteForm()
    return render(request, 'contenido/componente_form.html', {'form': form, 'actividad': actividad})


def editar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            return redirect('teaching_sequence')
    else:
        form = ActividadForm(instance=actividad)
    return render(request, 'contenido/actividad_form.html', {'form': form, 'actividad': actividad})


def editar_componente(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id)
    actividad = componente.actividad
    if request.method == 'POST':
        form = ComponenteForm(request.POST, instance=componente)
        if form.is_valid():
            form.save()
            return redirect('teaching_sequence')
    else:
        form = ComponenteForm(instance=componente)
    return render(request, 'contenido/componente_form.html', {'form': form, 'actividad': actividad, 'componente': componente})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # iniciar sesión automáticamente
            return redirect('teaching_sequence')
    else:
        form = UserCreationForm()

    return render(request, 'contenido/register.html', {'form': form})

def foro_detalle(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    comentarios = foro.comentarios.order_by("-fecha")

    if request.method == "POST":
        if request.user.is_authenticated:
            texto = request.POST.get("texto")
            if texto:
                Comentario.objects.create(
                    foro=foro,
                    usuario=request.user,
                    texto=texto
                )
                return redirect("foro_detalle", foro_id=foro.id)

    return render(request, "contenido/foro_detalle.html", {
        "foro": foro,
        "comentarios": comentarios
    })