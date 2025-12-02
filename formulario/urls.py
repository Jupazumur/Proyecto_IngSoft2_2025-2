from django.urls import path
from . import views

app_name = 'formulario'

urlpatterns = [
    path('nuevo/', views.crear_formulario, name='nuevo'),
    path('detalle/<int:pk>/', views.detalle_formulario, name='detalle'),
    path('editar/<int:pk>/', views.editar_formulario, name='editar'),
]
