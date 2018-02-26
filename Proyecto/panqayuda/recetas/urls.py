from django.urls import path
from . import views

urlpatterns = [
    # url(r'^$', views.agregar_receta, name='agregar_receta'),
    path('', views.lista_recetas, name='Lista de Recetas'),
    path('agregar_receta/', views.agregar_receta, name='Agregar Receta'),
]
