from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ventas'

urlpatterns = [

    path('', views.ventas, name='ventas'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
