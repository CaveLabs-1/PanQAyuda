from django.contrib import admin
from .models import Receta, RelacionRecetaMaterial, RecetaInventario

# Register your models here.
admin.site.register(Receta)
admin.site.register(RelacionRecetaMaterial)
admin.site.register(RecetaInventario)
