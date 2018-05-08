from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'materiales'

urlpatterns = [
    path('', views.lista_materiales_inventario, name='lista_materiales_inventario'),
    path('reporte', views.reporte, name='reporte'),
    path('lista_materiales', views.materiales, name='materiales'),
    path('lista_unidades', views.lista_unidades, name='lista_unidades'),
    path('lista_materiales/modificar_unidad/<int:id_unidad>', views.modificar_unidad, name='modificar_unidad'),
    path('agregar_unidades', views.agregar_unidades, name='agregar_unidades'),
    path('materiales_por_catalogo/', views.materiales_por_catalogo, name='materiales_por_catalogo'),
    path('lista_materiales/editar_material/<int:id_material>', views.editar_material, name='editar_material'),
    path('lista_materiales/eliminar_material/<int:id_material>', views.eliminar_material, name='eliminar_material'),
    path('lista_materiales/eliminar_unidad/<int:id_unidad>', views.eliminar_unidad, name='eliminar_unidad'),
    path('obtener_cantidad_inventario_con_caducados', views.obtener_cantidad_inventario_con_caducados,name='obtener_cantidad_inventario_con_caducados'),
    path('obtener_unidad_inventario_con_caducados', views.obtener_unidad_inventario_con_caducados,name='obtener_unidad_inventario_con_caducados'),
    path('obtener_cantidad_lote', views.obtener_cantidad_lote,name='obtener_cantidad_lote'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
