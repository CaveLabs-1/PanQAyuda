"""panqayuda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recetas import views as recetas_views
# from django.conf.urls import patterns, include, url

# from django.contrib.auth.decorators import login_required
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('agregar_receta/', 'recetas.urls'),
    path('recetas', recetas_views.recetas_list, name='index'),
]
