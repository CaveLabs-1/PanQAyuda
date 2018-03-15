from django.urls import path
from . import views

app_name = 'recetas'

urlpatterns = [
    # url(r'^$', views.agregar_receta, name='agregar_receta'),
    path('', views.lista_recetas, name=''),
    path('lista_recetas', views.lista_recetas, name='lista_de_recetas'),
    path('agregar_receta/', views.agregar_receta, name='agregar_receta'),
    path('receta/agregar_materiales/<int:id_receta>', views.agregar_materiales, name='agregar_materiales'),
    path('borrar_receta/<int:id_receta>', views.borrar_receta, name="borrar_receta"),
    path('agregar_materiales/borrar_material/<int:id_material>', views.borrar_material, name="borrar_material"),
    path('receta/agregar_materiales/borrar_material/<int:id_material>', views.borrar_material, name="borrar_material"),
    path('receta/borrar_receta/<int:id_receta>', views.borrar_receta, name="borrar_material"),
    path('receta/<int:id_receta>', views.detallar_receta, name='detallar_receta'),
    path('receta/editar_receta/<int:id_receta>', views.editar_receta, name='editar_receta')
]
