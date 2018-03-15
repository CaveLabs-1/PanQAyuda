from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'proveedores'

urlpatterns = [
    path('lista_proveedores', views.lista_proveedores, name="lista_proveedores"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
