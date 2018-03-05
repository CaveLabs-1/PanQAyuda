from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Receta(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=False)
    cantidad = models.IntegerField(null=True, blank=False, validators=[MinValueValidator(1, "Debes seleccionar un número entero mayor a 0.")])
    duration = models.DurationField(null=True, blank=False)
    material = models.ManyToManyField('materiales.Material', through = 'RelacionRecetaMaterial')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
    status = models.IntegerField(default=1)

class RelacionRecetaMaterial(models.Model):
    receta = models.ForeignKey('Receta', on_delete = models.CASCADE)
    material = models.ForeignKey('materiales.Material',  on_delete = models.CASCADE)
    cantidad = models.DecimalField(null=True, blank=False,max_digits=10, decimal_places=5,
                                   validators=[MinValueValidator(0.000001, "Debes seleccionar una cantidad mayor a 0.")])
    status = models.IntegerField(default=1)
