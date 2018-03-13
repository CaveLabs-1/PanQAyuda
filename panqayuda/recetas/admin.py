from django.contrib import admin
from .models import Receta, RelacionRecetaMaterial

# Register your models here.
admin.site.register(Receta)
admin.site.register(RelacionRecetaMaterial)
