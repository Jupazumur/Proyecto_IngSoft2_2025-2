from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from contenido.models import Actividad, Componente
from intento.models import Intento

@login_required
def lista_intentos(request):
    """
    Vista que muestra todos los Intentos organizados por Actividad y Componente.
    """
    # Obtener todas las actividades con sus componentes e intentos
    actividades = Actividad.objects.prefetch_related(
        'componentes__intentos__usuario'
    ).all()
    
    # Estructura de datos para el template
    actividades_data = []
    
    for actividad in actividades:
        componentes_data = []
        
        for componente in actividad.componentes.all():
            # Solo mostrar componentes que tienen intentos
            intentos = componente.intentos.all()
            
            if intentos.exists() or request.user.is_staff:
                componentes_data.append({
                    'componente': componente,
                    'intentos': intentos,
                    'total_intentos': intentos.count()
                })
        
        # Solo incluir actividades que tienen componentes con intentos
        if componentes_data or request.user.is_staff:
            actividades_data.append({
                'actividad': actividad,
                'componentes': componentes_data
            })
    
    return render(request, 'intento/lista_intentos.html', {
        'actividades_data': actividades_data
    })