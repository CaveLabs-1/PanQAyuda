from django.db import models
from recetas.models import Receta

class MermaReceta(models.Model):
    #id receta que se mermó
    id = models.ForeignKey(Receta, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, blank=False)
    fecha = models.DateTimeField(blank=True, null=False)
    descripcion = models.CharField(max_length=500, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.fecha + self.id 
# Create your models here.
