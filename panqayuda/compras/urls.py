from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'compras'

urlpatterns = [

    path('', views.compras, name='compras'),
    path('lista_detalle_compra/', views.lista_detalle_compra, name='lista_detalle_compra'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
