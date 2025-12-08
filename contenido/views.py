from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, modelform_factory

from .models import Actividad, Foro, Comentario, Componente, Examen, Cuestionario, BloqueApoyo, GlosarioGlobal
from formulario.models import Formulario, Pregunta, Respuesta, Opcion
from intento.models import Intento
from .forms import ActividadForm, ComponenteForm, ForoForm, ExamenDescForm, CuestionarioDescForm, BloqueApoyoForm

def editar_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    FormularioForm = modelform_factory(Formulario, fields=('nombre', 'descripcion'))

    PreguntaFormSet = inlineformset_factory(
        Formulario,
        Pregunta,
        fields=('texto', 'tipo'),
        extra=0,
        can_delete=True,
        prefix='preguntas'
    )

    if request.method == 'POST':
        form = FormularioForm(request.POST, instance=formulario)
        formset = PreguntaFormSet(request.POST, instance=formulario, prefix='preguntas')

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('teaching_sequence')
    else:
        form = FormularioForm(instance=formulario)
        formset = PreguntaFormSet(instance=formulario, prefix='preguntas')

    return render(request, 'formulario/formulario_form.html', {
        'form': form,
        'preguntas_formset': formset,
    })

def examen_detalle(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id, tipo="examen")
    examen = get_object_or_404(Examen, componente=componente)
    formulario = componente.formulario
    preguntas = formulario.preguntas.prefetch_related('opciones').all() if formulario else []
    mensaje = None
    puede_acceder = puede_acceder_componente(request, componente)

    if request.method == "POST":
        if not request.user.is_authenticated:
            mensaje = "Debes iniciar sesión para responder el examen."
        elif not puede_acceder:
            mensaje = f"Has agotado el número máximo de intentos ({examen.max_intentos}) para este examen."
        else:
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
            return redirect('intento_resultado', intento_id=intento.id)

    return render(request, "contenido/examen_detalle.html", {
        "componente": componente,
        "examen": examen,
        "formulario": formulario,
        "preguntas": preguntas,
        "mensaje": mensaje,
        "puede_acceder": puede_acceder,
    })

def cuestionario_detalle(request, componente_id):
    componente = get_object_or_404(Componente, id=componente_id, tipo="cuestionario")
    cuestionario = get_object_or_404(Cuestionario, componente=componente)
    formulario = componente.formulario
    preguntas = formulario.preguntas.prefetch_related('opciones').all() if formulario else []
    mensaje = None
    puede_acceder = puede_acceder_componente(request, componente)

    if request.method == "POST":
        if not request.user.is_authenticated:
            mensaje = "Debes iniciar sesión para responder el cuestionario."
        elif not puede_acceder:
            mensaje = f"Has agotado el número máximo de intentos ({cuestionario.max_intentos}) para este cuestionario."
        else:
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
            return redirect('intento_resultado', intento_id=intento.id)

    return render(request, "contenido/cuestionario_detalle.html", {
        "componente": componente,
        "cuestionario": cuestionario,
        "formulario": formulario,
        "preguntas": preguntas,
        "mensaje": mensaje,
        "puede_acceder": puede_acceder,
    })

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
        form.fields.pop('formulario', None)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.actividad = actividad
            comp.save()
            
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
                    pass
            
            return redirect('teaching_sequence')
    else:
        form = ComponenteForm()
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
    
    examen = None
    cuestionario = None
    if componente.tipo == "examen" and hasattr(componente, 'examen'):
        examen = componente.examen
    elif componente.tipo == "cuestionario" and hasattr(componente, 'cuestionario'):
        cuestionario = componente.cuestionario
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = ComponenteForm(post_data, instance=componente)
        form.fields.pop('tipo', None)
        form.fields.pop('formulario', None)
        if form.is_valid():
            form.save()
            
            if componente.tipo == "examen" and examen:
                max_intentos = request.POST.get('max_intentos')
                if max_intentos:
                    try:
                        examen.max_intentos = int(max_intentos)
                        examen.save(update_fields=['max_intentos'])
                    except ValueError:
                        pass
            elif componente.tipo == "cuestionario" and cuestionario:
                max_intentos = request.POST.get('max_intentos')
                if max_intentos:
                    try:
                        cuestionario.max_intentos = int(max_intentos)
                        cuestionario.save(update_fields=['max_intentos'])
                    except ValueError:
                        pass
            
            return redirect('teaching_sequence')
    else:
        form = ComponenteForm(instance=componente)
        form.fields.pop('tipo', None)
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
            login(request, user)
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

def puede_acceder_componente(request, componente):
    if not request.user.is_authenticated:
        return True 

    intentos_usuario = Intento.objects.filter(
        usuario=request.user,
        componente=componente
    ).count()

    if componente.tipo == "examen" and hasattr(componente, 'examen'):
        max_intentos = componente.examen.max_intentos
    elif componente.tipo == "cuestionario" and hasattr(componente, 'cuestionario'):
        max_intentos = componente.cuestionario.max_intentos
    else:
        return True

    return intentos_usuario < max_intentos

def intento_resultado(request, intento_id):
    intento = get_object_or_404(Intento, id=intento_id)
    
    if request.user != intento.usuario and not request.user.is_staff:
        from django.http import Http404
        raise Http404("No tienes permiso para ver este intento.")
    
    componente = intento.componente
    formulario = componente.formulario
    preguntas = formulario.preguntas.prefetch_related('opciones').all() if formulario else []
    
    respuestas_intento = {resp.pregunta.id: resp for resp in intento.respuestas.select_related('pregunta', 'opcion').all()}
    
    resultados = []
    total_preguntas = len(preguntas)
    preguntas_correctas = 0
    preguntas_incorrectas = 0
    preguntas_abiertas = 0
    
    for pregunta in preguntas:
        respuesta_usuario = respuestas_intento.get(pregunta.id)
        
        resultado_pregunta = {
            'pregunta': pregunta,
            'respuesta_usuario': respuesta_usuario,
            'es_correcta': None,
            'opcion_correcta': None,
        }
        
        if pregunta.tipo == 'opcion_multiple':
            if respuesta_usuario and respuesta_usuario.opcion:
                resultado_pregunta['es_correcta'] = respuesta_usuario.opcion.correcta
                if resultado_pregunta['es_correcta']:
                    preguntas_correctas += 1
                else:
                    preguntas_incorrectas += 1
                
                opcion_correcta = pregunta.opciones.filter(correcta=True).first()
                resultado_pregunta['opcion_correcta'] = opcion_correcta
            else:
                preguntas_incorrectas += 1
                opcion_correcta = pregunta.opciones.filter(correcta=True).first()
                resultado_pregunta['opcion_correcta'] = opcion_correcta
        else:
            preguntas_abiertas += 1
            resultado_pregunta['es_correcta'] = None
        
        resultados.append(resultado_pregunta)
    
    examen = None
    cuestionario = None
    tipo_componente = None
    titulo_componente = None
    
    if componente.tipo == "examen" and hasattr(componente, 'examen'):
        examen = componente.examen
        tipo_componente = "examen"
        titulo_componente = examen.titulo
    elif componente.tipo == "cuestionario" and hasattr(componente, 'cuestionario'):
        cuestionario = componente.cuestionario
        tipo_componente = "cuestionario"
        titulo_componente = cuestionario.titulo
    
    preguntas_opcion_multiple = total_preguntas - preguntas_abiertas
    porcentaje_aciertos = None
    if preguntas_opcion_multiple > 0:
        porcentaje_aciertos = round((preguntas_correctas / preguntas_opcion_multiple) * 100, 2)
    
    return render(request, "contenido/intento_resultado.html", {
        "intento": intento,
        "componente": componente,
        "examen": examen,
        "cuestionario": cuestionario,
        "tipo_componente": tipo_componente,
        "titulo_componente": titulo_componente,
        "resultados": resultados,
        "total_preguntas": total_preguntas,
        "preguntas_correctas": preguntas_correctas,
        "preguntas_incorrectas": preguntas_incorrectas,
        "preguntas_abiertas": preguntas_abiertas,
        "preguntas_opcion_multiple": preguntas_opcion_multiple,
        "porcentaje_aciertos": porcentaje_aciertos,
    })