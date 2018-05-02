from django.contrib import admin
from .models import Venta
from .models import RelacionVentaPaquete


admin.site.register(Venta)
admin.site.register(RelacionVentaPaquete)
