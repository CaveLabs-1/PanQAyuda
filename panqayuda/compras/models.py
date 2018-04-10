from django.db import models
from django.utils import timezone
from proveedores.models import Proveedor
from django.core.validators import MinValueValidator

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    materiales = models.ManyToManyField('materiales.MaterialInventario', through = 'RelacionCompraMaterial')
    fecha_compra = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.proveedor.nombre
# Create your models here.

class RelacionCompraMaterial(models.Model):
    compra = models.ForeignKey('Compra', on_delete = models.CASCADE)
    material = models.ForeignKey('materiales.MaterialInventario',  on_delete = models.CASCADE)
    cantidad = models.DecimalField(null=True, blank=False,max_digits=10, decimal_places=5,
                                   validators=[MinValueValidator(0.000001, "Debes seleccionar una cantidad mayor a 0.")])
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.material.nombre
