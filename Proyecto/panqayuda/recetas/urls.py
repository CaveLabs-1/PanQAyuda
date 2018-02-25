from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.agregar_receta, name='agregar_receta'),
    path('', views.index, name='index'),
    path('agregar_receta/', views.agregar_receta),
]
