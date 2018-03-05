from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'paquetes'

urlpatterns = [
    path('lista_paquetes/', views.lista_paquetes, name='lista_paquetes'),
    path('agregar_paquete/', views.agregar_paquete, name='agregar_paquete'),
    path('agregar_recetas_a_paquete/<int:id_paquete>/', views.agregar_recetas_a_paquete, name='agregar_recetas_a_paquete'),
    path('agregar_receta_a_paquete/', views.agregar_receta_a_paquete, name='agregar_receta_a_paquete'),
    path('lista_paquetes/editar_paquete/<int:id_paquete>', views.editar_paquete, name='editar_paquete'),
    path('agregar_inventario/', views.agregar_paquete_inventario, name='agregar_inventario'),
    #path('prueba_view/', views.prueba_view, name='prueba_view')
    #path('prueba_view/', views.prueba_view, name='prueba_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
