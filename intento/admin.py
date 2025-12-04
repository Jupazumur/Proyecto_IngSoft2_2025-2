from django.contrib import admin
from .models import Intento

@admin.register(Intento)
class IntentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'componente', 'fecha_creacion', 'tipo_componente')
    list_filter = ('fecha_creacion', 'componente__tipo')
    search_fields = ('usuario__username', 'componente__titulo')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    def tipo_componente(self, obj):
        return obj.componente.get_tipo_display()
    tipo_componente.short_description = 'Tipo'