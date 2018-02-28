from django.urls import path
from . import views

urlpatterns = [
    # url(r'^$', views.agregar_receta, name='agregar_receta'),
    path('', views.lista_recetas, name='lista_de_recetas'),
    path('agregar_receta/', views.agregar_receta, name='agregar_receta'),
    path('agregar_materiales/<int:id_receta>', views.agregar_materiales, name='agregar_materiales'),
    path('borrar_receta/<int:id_receta>', views.borrar_receta, name="borrar_receta"),
    path('agregar_materiales/borrar_material/<int:id_material>', views.borrar_material, name="borrar_material"),
    path('receta/<int:id_receta>', views.detallar_receta, name='detallar_receta'),
    # path('editar_receta/<int:pk>', views.EditarReceta.as_view(), name='editar_receta')
]
