from django.db import models
from compras.models import Compra
from django.utils import timezone
import datetime

# Create your models here.
class Material(models.Model):#¿Tiene unidad?
    nombre = models.CharField(max_length=100, null=True, blank=False)
    codigo = models.CharField(max_length=10, null=True, blank=False)
    status = models.IntegerField(default=1)
    #Agregar campo de relación unidad-porcion
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def obtener_cantidad_inventario(self):
        return MaterialInventario.filter(material=self,
            deleted_at__isnull=True, fecha_cad__gte=datetime.datetime.now(),
            cantidad_disponible__gt=0).aggregate(cantidad_disponible=Sum('cantidad_disponible'))['cantidad_total']

#Modelo
class Unidad(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class MaterialInventario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    unidad_entrada = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default = 0)
    cantidad_salida = models.IntegerField(default = 0)
    cantidad_disponible = models.IntegerField(default = 0)
    costo = models.FloatField(blank=True, null="True")
    fecha_cad = models.DateTimeField(blank=True, null="True")
    estatus = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.material.nombre
