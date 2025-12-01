from django.urls import path

from . import views

urlpatterns = [
    path('', views.teaching_sequence, name='teaching_sequence'),
    path('actividad/nueva/', views.crear_actividad, name='crear_actividad'),
    path('actividad/<int:actividad_id>/editar/', views.editar_actividad, name='editar_actividad'),
    path('foro/<int:foro_id>/', views.foro_detalle, name='foro_detalle'),
    path('foro/<int:foro_id>/editar/', views.editar_foro, name='editar_foro'),
    path('examen/<int:componente_id>/editar-desc/', views.editar_examen_desc, name='editar_examen_desc'),
    path('cuestionario/<int:componente_id>/editar-desc/', views.editar_cuestionario_desc, name='editar_cuestionario_desc'),
    path('examen/<int:componente_id>/', views.examen_detalle, name='examen_detalle'),
    path('cuestionario/<int:componente_id>/', views.cuestionario_detalle, name='cuestionario_detalle'),
    path('actividad/<int:actividad_id>/componente/nuevo/', views.agregar_componente, name='agregar_componente'),
    path('componente/<int:componente_id>/editar/', views.editar_componente, name='editar_componente'),
    path('register/', views.register, name='register'),
]
