from django.db import models
from django.utils import timezone

class Receta(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=False)
    cantidad = models.IntegerField()
    duration = models.DurationField()
    material = models.ManyToManyField('materiales.Material', through = 'RelacionRecetaMaterial')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
    status = models.IntegerField(default=1)

class RelacionRecetaMaterial(models.Model):
    receta = models.ForeignKey('Receta', on_delete = models.CASCADE)
    material = models.ForeignKey('materiales.Material',  on_delete = models.CASCADE)
    cantidad = models.PositiveIntegerField()
    status = models.IntegerField(default=1)
