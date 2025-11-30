from django.contrib import admin

from django.contrib import admin
from .models import Actividad, Componente, Foro, Comentario, Examen, Cuestionario

admin.site.register(Actividad)
admin.site.register(Componente)
admin.site.register(Foro)
admin.site.register(Comentario)
admin.site.register(Examen)
admin.site.register(Cuestionario)