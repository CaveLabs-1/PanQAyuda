from django.db import models
from django.utils import timezone

class Receta(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=False)
    cantidad = models.IntegerField()
    duracion = models.DurationField()
    material = models.ManyToManyField('materiales.Material')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
