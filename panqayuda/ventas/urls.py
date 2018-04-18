from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ventas'

urlpatterns = [

    path('', views.ventas, name='ventas'),
    path('lista_detalle_venta/', views.lista_detalle_venta, name='lista_detalle_venta'),
    path('agergar_paquete_a_venta/', views.agregar_paquete_a_venta, name='agregar_paquete_a_venta'),
    path('generar_venta/', views.generar_venta, name='generar_venta'),
    path('cancelar_venta/<int:id_venta>', views.cancelar_venta, name='cancelar_venta'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
