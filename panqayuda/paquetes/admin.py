from django.contrib import admin

from .models import Paquete, RecetasPorPaquete, PaqueteInventario

admin.site.register(Paquete)
admin.site.register(RecetasPorPaquete)
admin.site.register(PaqueteInventario)
