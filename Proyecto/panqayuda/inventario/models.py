from django.db import models
from django.utils import timezone

class Receta(models.Model):
    idMaterial = models.IntegerField()
    cantidad = models.IntegerField()
    idCompra = models.IntegerField()
    fecha_caducidad = models.DateTimeField(blank = True, null = True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
