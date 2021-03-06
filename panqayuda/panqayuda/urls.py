"""panqayuda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based viewsda
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout


# from django.conf.urls import patterns, include, url

# from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', include('ventas.urls', namespace='index')),
    path('admin/', admin.site.urls),
    path('recetas/', include('recetas.urls', namespace='recetas')),
    path('paquetes/', include('paquetes.urls', namespace='paquetes')),
    path('ordenes/', include('ordenes.urls', namespace='ordenes')),
    path('', include('django.contrib.auth.urls'), {'template_name': 'login/login.html'},name='login'),
    path('', include('django.contrib.auth.urls')),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path('proveedores/', include('proveedores.urls', namespace='proveedores')),
    path('materiales/', include('materiales.urls', namespace='materiales')),
    path('compras/', include('compras.urls', namespace='compras')),
    path('ventas/', include('ventas.urls', namespace='ventas')),
    path('mermas/', include('mermas.urls', namespace='mermas')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),

]
