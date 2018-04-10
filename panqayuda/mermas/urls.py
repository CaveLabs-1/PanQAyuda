from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mermas'

urlpatterns = [
    path('recetas', views.lista_mermas_receta, name='lista_mermas_receta'),
    path('paquetes', views.lista_mermas_paquete, name='lista_mermas_paquete'),
    path('materiales', views.lista_mermas_material, name='lista_mermas_material'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
