from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'materiales'

urlpatterns = [

    path('', views.lista_materiales_inventario, name='lista_materiales_inventario'),
    path('lista_materiales', views.materiales, name='materiales'),
    path('lista_unidades', views.lista_unidades, name='lista_unidades'),
    path('agregar_unidades', views.agregar_unidades, name='agregar_unidades'),
    path('materiales_por_catalogo/', views.materiales_por_catalogo, name='materiales_por_catalogo'),


    # path('editar_material/<int:id_cliente>', views.editar_cliente, name='editar_cliente'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
