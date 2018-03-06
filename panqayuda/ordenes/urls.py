from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ordenes'

urlpatterns = [
    path('', views.ordenes, name='ordenes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
