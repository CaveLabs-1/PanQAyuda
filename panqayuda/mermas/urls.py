from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mermas'

urlpatterns = [
    path('lista_mermas/', views.lista_mermas_paquete, name='lista_mermas_paquete'),
    path('lista_mermas/agregar_merma_paquetes', views.agregar_merma_paquetes, name='agregar_merma_paquetes'),
    path('lista_mermas_receta/', views.lista_mermas_receta, name='lista_mermas_receta'),
    path('lista_mermas_material/', views.lista_mermas_material, name='lista_mermas_material'),
    path('lista_mermas_material/agregar_merma_materiales', views.agregar_merma_materiales, name='agregar_merma_materiales'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
