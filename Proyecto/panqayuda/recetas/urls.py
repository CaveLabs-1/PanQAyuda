from django.urls import path
from . import views

urlpatterns = [
    # url(r'^$', views.agregar_receta, name='agregar_receta'),
    path('', views.lista_recetas, name='lista_de_recetas'),
    path('agregar_receta/', views.agregar_receta, name='agregar_receta'),
    path('agregar_materiales/<int:id_receta>', views.agregar_materiales, name='agregar_materiales'),
    path('borrar_material/<int:id_receta>', views.borrar_material, name="borrar_material")
]
