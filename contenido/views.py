from django.shortcuts import render, get_object_or_404, redirect
from .models import Actividad, Foro, Comentario, Componente, Examen, Cuestionario, BloqueApoyo, GlosarioGlobal
from formulario.models import Formulario
from .forms import ActividadForm, ComponenteForm, ForoForm, ExamenDescForm, CuestionarioDescForm, BloqueApoyoForm

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
            from intento.models import Intento
            
            # Crear un Intento para agrupar todas las respuestas
            intento = Intento.objects.create(
                usuario=request.user,
                componente=componente
            )

            for pregunta in preguntas:
                key = f"pregunta_{pregunta.id}"
                valor = request.POST.get(key)
                if pregunta.tipo == 'abierta':
                    if valor:
                        Respuesta.objects.create(
                            pregunta=pregunta,
                            texto=valor,
                            usuario=request.user.username,
                            intento=intento
                        )
                elif pregunta.tipo == 'opcion_multiple':
                    if valor:
                        opcion = Opcion.objects.filter(id=valor, pregunta=pregunta).first()
                        Respuesta.objects.create(
                            pregunta=pregunta,
                            opcion=opcion,
                            usuario=request.user.username,
                            intento=intento
                        )
            mensaje = "Respuestas enviadas correctamente."

    return render(request, "contenido/examen_detalle.html", {
        "componente": componente,
        "examen": examen,
        "formulario": formulario,
        "preguntas": preguntas,
        "mensaje": mensaje,
    })

def cuestionario_detalle(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id, tipo="cuestionario")
    cuestionario = get_object_or_404(Cuestionario, componente=componente)
    formulario = componente.formulario
    preguntas = formulario.preguntas.prefetch_related('opciones').all() if formulario else []
    mensaje = None

    if request.method == "POST":
        if not request.user.is_authenticated:
            mensaje = "Debes iniciar sesión para responder el cuestionario."
        else:
            from formulario.models import Respuesta, Opcion
            from intento.models import Intento
            
            # Crear un Intento para agrupar todas las respuestas
            intento = Intento.objects.create(
                usuario=request.user,
                componente=componente
            )

            for pregunta in preguntas:
                key = f"pregunta_{pregunta.id}"
                valor = request.POST.get(key)
                if pregunta.tipo == 'abierta':
                    if valor:
                        Respuesta.objects.create(
                            pregunta=pregunta,
                            texto=valor,
                            usuario=request.user.username,
                            intento=intento
                        )
                elif pregunta.tipo == 'opcion_multiple':
                    if valor:
                        opcion = Opcion.objects.filter(id=valor, pregunta=pregunta).first()
                        Respuesta.objects.create(
                            pregunta=pregunta,
                            opcion=opcion,
                            usuario=request.user.username,
                            intento=intento
                        )
            mensaje = "Respuestas enviadas correctamente."

    return render(request, "contenido/cuestionario_detalle.html", {
        "componente": componente,
        "cuestionario": cuestionario,
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
        # Excluir el campo formulario al crear
        form.fields.pop('formulario', None)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.actividad = actividad
            comp.save()
            
            # Actualizar max_intentos si es examen o cuestionario
            max_intentos = request.POST.get('max_intentos')
            if max_intentos and comp.tipo in ["examen", "cuestionario"]:
                try:
                    max_intentos_value = int(max_intentos)
                    if comp.tipo == "examen" and hasattr(comp, 'examen'):
                        comp.examen.max_intentos = max_intentos_value
                        comp.examen.save(update_fields=['max_intentos'])
                    elif comp.tipo == "cuestionario" and hasattr(comp, 'cuestionario'):
                        comp.cuestionario.max_intentos = max_intentos_value
                        comp.cuestionario.save(update_fields=['max_intentos'])
                except ValueError:
                    pass  # Si no es un número válido, ignorar
            
            return redirect('teaching_sequence')
    else:
        form = ComponenteForm()
        # Excluir el campo formulario al crear
        form.fields.pop('formulario', None)
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
    
    # Obtener el examen o cuestionario relacionado si existe
    examen = None
    cuestionario = None
    if componente.tipo == "examen" and hasattr(componente, 'examen'):
        examen = componente.examen
    elif componente.tipo == "cuestionario" and hasattr(componente, 'cuestionario'):
        cuestionario = componente.cuestionario
    
    if request.method == 'POST':
        # Excluir el campo tipo del POST para que no se pueda modificar
        post_data = request.POST.copy()
        form = ComponenteForm(post_data, instance=componente)
        # Excluir el campo tipo del formulario
        form.fields.pop('tipo', None)
        # Excluir el campo formulario (no se puede cambiar desde aquí, solo editar si existe)
        form.fields.pop('formulario', None)
        if form.is_valid():
            form.save()
            # titulo se sincroniza automaticamente mediante el signal post_save en models.py
            
            # Actualizar max_intentos si es examen o cuestionario
            if componente.tipo == "examen" and examen:
                max_intentos = request.POST.get('max_intentos')
                if max_intentos:
                    try:
                        examen.max_intentos = int(max_intentos)
                        examen.save(update_fields=['max_intentos'])
                    except ValueError:
                        pass  # Si no es un número válido, ignorar
            elif componente.tipo == "cuestionario" and cuestionario:
                max_intentos = request.POST.get('max_intentos')
                if max_intentos:
                    try:
                        cuestionario.max_intentos = int(max_intentos)
                        cuestionario.save(update_fields=['max_intentos'])
                    except ValueError:
                        pass  # Si no es un número válido, ignorar
            
            return redirect('teaching_sequence')
    else:
        form = ComponenteForm(instance=componente)
        # Excluir el campo tipo del formulario al editar
        form.fields.pop('tipo', None)
        # Excluir el campo formulario (no se puede cambiar desde aquí, solo editar si existe)
        form.fields.pop('formulario', None)
    return render(request, 'contenido/componente_form.html', {
        'form': form, 
        'actividad': actividad, 
        'componente': componente,
        'examen': examen,
        'cuestionario': cuestionario
    })

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


def editar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    if request.method == 'POST':
        form = ForoForm(request.POST, instance=foro)
        if form.is_valid():
            form.save()
            return redirect('foro_detalle', foro_id=foro.id)
    else:
        form = ForoForm(instance=foro)
    return render(request, 'contenido/editar_foro.html', {'form': form, 'foro': foro})

def editar_examen_desc(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id, tipo="examen")
    examen = get_object_or_404(Examen, componente=componente)

    if request.method == "POST":
        form = ExamenDescForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            return redirect("examen_detalle", componente_id=componente.id)
    else:
        form = ExamenDescForm(instance=examen)

    return render(request, "contenido/editar_desc.html", {
        "form": form,
        "examen": examen,
    })


def editar_cuestionario_desc(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id, tipo="cuestionario")
    cuestionario = get_object_or_404(Cuestionario, componente=componente)

    if request.method == "POST":
        form = CuestionarioDescForm(request.POST, instance=cuestionario)
        if form.is_valid():
            form.save()
            return redirect("cuestionario_detalle", componente_id=componente.id)
    else:
        form = CuestionarioDescForm(instance=cuestionario)

    return render(request, "contenido/editar_desc.html", {
        "form": form,
        "cuestionario": cuestionario,
    })


def eliminar_componente(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id)
    if request.method == 'POST':
        componente.delete()
        return redirect('teaching_sequence')
    return render(request, 'contenido/eliminar_componente_confirmar.html', {'componente': componente})


def eliminar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if request.method == 'POST':
        actividad.delete()
        return redirect('teaching_sequence')
    return render(request, 'contenido/eliminar_actividad_confirmar.html', {'actividad': actividad})

def editar_glosario_global(request):
    glosario = GlosarioGlobal.objects.last()
    
    # Si no existe, lo crea al vuelo
    if not glosario:
        glosario = GlosarioGlobal.objects.create(titulo="Recursos del Curso", contenido="")

    if not request.user.is_staff:
        return redirect('teaching_sequence')

    if request.method == 'POST':
        form = BloqueApoyoForm(request.POST, instance=glosario)
        if form.is_valid():
            form.save()
            return redirect('teaching_sequence')
    else:
        form = BloqueApoyoForm(instance=glosario)

    return render(request, 'contenido/bloque_form.html', {'form': form})