from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'compras'

urlpatterns = [

    path('', views.compras, name='compras'),
    path('lista_detalle_compra/', views.lista_detalle_compra, name='lista_detalle_compra'),
    path('agregar_compra' , views.agregar_compra, name='agregar_compra'),
    path('agregar_materias_primas_a_compra/<int:id_compra>', views.agregar_materias_primas_a_compra, name='agregar_materias_primas_a_compra'),
    path('agregar_materia_prima_a_compra/', views.agregar_materia_prima_a_compra, name='agregar_materia_prima_a_compra'),
    path('eliminar_compra/<int:id_compra>', views.eliminar_compra, name='eliminar_compra'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
