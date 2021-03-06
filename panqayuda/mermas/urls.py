from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mermas'

urlpatterns = [
    path('lista_mermas/', views.lista_mermas_paquete, name='lista_mermas_paquete'),
    path('lista_mermas/agregar_merma_paquetes', views.agregar_merma_paquetes, name='agregar_merma_paquetes'),
    path('lista_mermas_receta/', views.lista_mermas_receta, name='lista_mermas_receta'),
    path('lista_mermas_receta/agregar_merma_recetas', views.agregar_merma_recetas, name='agregar_merma_recetas'),
    path('lista_mermas_material/', views.lista_mermas_material, name='lista_mermas_material'),
    path('lista_mermas_material/agregar_merma_materiales', views.agregar_merma_materiales, name='agregar_merma_materiales'),
    path('obtener_paquetes_ajuste_inventario', views.obtener_paquetes_ajuste_inventario, name='obtener_paquetes_ajuste_inventario'),
    path('obtener_recetas_ajuste_inventario', views.obtener_recetas_ajuste_inventario,name='obtener_recetas_ajuste_inventario'),
    path('obtener_materiales_ajuste_inventario', views.obtener_materiales_ajuste_inventario,name='obtener_materiales_ajuste_inventario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
