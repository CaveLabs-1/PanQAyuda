from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'clientes'

urlpatterns = [
    path('', views.clientes, name='clientes'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
