from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mermas'

urlpatterns = [
    path('lista_mermas/', views.agregar_merma_paquetes, name='mermas_paquetes'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
