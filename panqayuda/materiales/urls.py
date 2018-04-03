from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'materiales'

urlpatterns = [
    path('agregar_unidades', views.agregar_unidades, name='agregar_unidades'),
    path('', views.materiales, name='materiales'),
    path('lista_unidades', views.lista_unidades, name='lista_unidades'),
    # path('editar_material/<int:id_cliente>', views.editar_cliente, name='editar_cliente'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
