from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('borrar_usuario/<int:id_usuario>', views.borrar_usuario, name='borrar_usuario'),
]
