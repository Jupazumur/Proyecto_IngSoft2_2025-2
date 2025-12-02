from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.safestring import mark_safe
from .models import Formulario, Pregunta, Opcion
import json


@require_http_methods(["GET", "POST"])
def crear_formulario(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		descripcion = request.POST.get('descripcion', '').strip()
		if nombre:
			formulario = Formulario.objects.create(nombre=nombre, descripcion=descripcion)
			textos = request.POST.getlist('pregunta_text')
			tipos = request.POST.getlist('pregunta_tipo')
			opciones_list = request.POST.getlist('pregunta_opciones')
			for i, texto in enumerate(textos):
				texto = texto.strip()
				if not texto:
					continue
				tipo = tipos[i] if i < len(tipos) else 'abierta'
				pregunta = Pregunta.objects.create(formulario=formulario, texto=texto, tipo=tipo)
				if tipo == 'opcion_multiple':
					opciones_raw = opciones_list[i] if i < len(opciones_list) else ''
					# soporte para JSON enviado desde el frontend: [{text:..., correct: true}, ...]
					opts = []
					try:
						opts = json.loads(opciones_raw)
					except Exception:
						# compatibilidad: cadena separada por comas
						opts = [{'text': o.strip(), 'correct': False} for o in opciones_raw.split(',') if o.strip()]
					# asegurar que sólo una opción sea correcta (siempre la primera marcada)
					found = False
					for opt in opts:
						if isinstance(opt, dict):
							if opt.get('correct') and not found:
								found = True
							else:
								opt['correct'] = False
					for opt in opts:
						texto_opt = (opt.get('text') if isinstance(opt, dict) else str(opt)).strip()
						if not texto_opt:
							continue
						correcta = False
						if isinstance(opt, dict):
							correcta = bool(opt.get('correct', False))
						Opcion.objects.create(pregunta=pregunta, texto=texto_opt, correcta=correcta)
			return redirect('formulario:detalle', pk=formulario.pk)
	return render(request, 'formulario/formulario_form.html')


def detalle_formulario(request, pk):
	formulario = get_object_or_404(Formulario, pk=pk)
	return render(request, 'formulario/formulario_detail.html', {'formulario': formulario})


@require_http_methods(["GET", "POST"])
def editar_formulario(request, pk):
	formulario = get_object_or_404(Formulario, pk=pk)
	
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		descripcion = request.POST.get('descripcion', '').strip()
		if nombre:
			formulario.nombre = nombre
			formulario.descripcion = descripcion
			formulario.save()
			
			# Eliminar preguntas existentes
			formulario.preguntas.all().delete()
			
			# Crear nuevas preguntas
			textos = request.POST.getlist('pregunta_text')
			tipos = request.POST.getlist('pregunta_tipo')
			opciones_list = request.POST.getlist('pregunta_opciones')
			for i, texto in enumerate(textos):
				texto = texto.strip()
				if not texto:
					continue
				tipo = tipos[i] if i < len(tipos) else 'abierta'
				pregunta = Pregunta.objects.create(formulario=formulario, texto=texto, tipo=tipo)
				if tipo == 'opcion_multiple':
					opciones_raw = opciones_list[i] if i < len(opciones_list) else ''
					# soporte para JSON enviado desde el frontend: [{text:..., correct: true}, ...]
					opts = []
					try:
						opts = json.loads(opciones_raw)
					except Exception:
						# compatibilidad: cadena separada por comas
						opts = [{'text': o.strip(), 'correct': False} for o in opciones_raw.split(',') if o.strip()]
					# asegurar que sólo una opción sea correcta (siempre la primera marcada)
					found = False
					for opt in opts:
						if isinstance(opt, dict):
							if opt.get('correct') and not found:
								found = True
							else:
								opt['correct'] = False
					for opt in opts:
						texto_opt = (opt.get('text') if isinstance(opt, dict) else str(opt)).strip()
						if not texto_opt:
							continue
						correcta = False
						if isinstance(opt, dict):
							correcta = bool(opt.get('correct', False))
						Opcion.objects.create(pregunta=pregunta, texto=texto_opt, correcta=correcta)
			return redirect('formulario:detalle', pk=formulario.pk)
	
	# Preparar datos para el template
	preguntas_data = []
	for pregunta in formulario.preguntas.all():
		opciones_data = []
		for opcion in pregunta.opciones.all():
			opciones_data.append({
				'text': opcion.texto,
				'correct': opcion.correcta
			})
		preguntas_data.append({
			'texto': pregunta.texto,
			'tipo': pregunta.tipo,
			'opciones': opciones_data
		})
	
	# Convertir a JSON seguro para el template
	preguntas_data_json = mark_safe(json.dumps(preguntas_data))
	
	return render(request, 'formulario/formulario_form.html', {
		'formulario': formulario,
		'preguntas_data_json': preguntas_data_json
	})