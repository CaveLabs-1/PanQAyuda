from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'paquetes'

urlpatterns = [
    path('', views.lista_paquete_inventario, name='lista_paquete_inventario'),
    path('borrar_paquete_inventario/<int:id_paquete_inventario>', views.borrar_paquete_inventario, name='borrar_paquete_inventario'),
    path('lista_paquetes/', views.lista_paquetes, name='lista_paquetes'),
    path('agregar_paquete/', views.agregar_paquete, name='agregar_paquete'),
    path('agregar_recetas_a_paquete/<int:id_paquete>/', views.agregar_recetas_a_paquete, name='agregar_recetas_a_paquete'),
    path('agregar_receta_a_paquete/', views.agregar_receta_a_paquete, name='agregar_receta_a_paquete'),
    path('lista_paquetes/borrar_paquete/<int:id_paquete>', views.borrar_paquete, name='borrar_paquete'),
    path('lista_paquetes/editar_paquete/<int:id_paquete>', views.editar_paquete, name='editar_paquete'),
    path('editar_paquete_inventario/<int:id_paquete>', views.editar_paquete_inventario, name='editar_paquete_inventario'),
    path('agregar_paquete_inventario/', views.agregar_paquete_inventario, name='agregar_inventario'),
    path('agregar_inventario/', views.agregar_paquete_inventario, name='agregar_inventario'),
    path('paquetes_por_catalogo/', views.paquetes_por_catalogo, name='paquetes_por_catalogo'),
    path('borrar_paquete_inventario/<int:id_paquete>', views.borrar_paquete_inventario, name='borrar_paquete_inventario'),
    path('quitar_receta_paquete', views.quitar_receta_paquete, name='quitar_receta_paquete'),
    path('obtener_cantidad_inventario/', views.obtener_cantidad_inventario, name='obtener_cantidad_inventario'),
    path('obtener_cantidad_inventario_con_caducados/', views.obtener_cantidad_inventario_con_caducados,name='obtener_cantidad_inventario_con_caducados'),
    path('obtener_cantidad_lote/', views.obtener_cantidad_lote,name='obtener_cantidad_lote'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
