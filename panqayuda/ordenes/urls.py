from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ordenes'

urlpatterns = [
    path('', views.ordenes, name='ordenes'),
    path('terminar_orden', views.terminar_orden, name='terminar_orden'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
