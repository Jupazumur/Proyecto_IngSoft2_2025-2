from .models import GlosarioGlobal

def glosario_global(request):
    # Busca el último glosario creado en la base de datos
    glosario = GlosarioGlobal.objects.last()
    # Se lo entrega a todas las plantillas HTML
    return {'glosario_global': glosario}