from django.contrib import admin
from .models import Paquete, PaqueteInventario, RecetasPorPaquete

admin.site.register(Paquete)
admin.site.register(PaqueteInventario)
admin.site.register(RecetasPorPaquete)
# Register your models here.
