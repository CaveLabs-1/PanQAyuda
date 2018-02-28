from django.db import models
from django.utils import timezone

class Orden(models.Model)
    idReceta = models.IntegerField()
    cantidad = models.IntegerField()
    estatus = models.IntegerField()
    fecha_fin = models.DateTimeField(blank = True, null = True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
