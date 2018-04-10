from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'compras'

urlpatterns = [

    path('' , views.lista_compras, name='lista_compras'),
    path('agregar_compra' , views.agregar_compra, name='agregar_compra'),
    path('agregar_materias_primas_a_compra/<int:id_compra>', views.agregar_materias_primas_a_compra, name='agregar_materias_primas_a_compra'),
    path('agregar_materia_prima_a_compra/', views.agregar_materia_prima_a_compra, name='agregar_materia_prima_a_compra'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
