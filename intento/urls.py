from django.urls import path
from . import views

urlpatterns = [
    path('intentos/', views.lista_intentos, name='lista_intentos'),
]
