from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'proveedores'

urlpatterns = [
    path('lista_proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('agregar_proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedor/<int:id_proveedor>', views.detallar_proveedor, name='detallar_proveedor'),
    path('lista_proveedores/eliminar_proveedor/<int:id_proveedor>', views.eliminar_proveedor, name='eliminar_proveedor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
