from django.db import models
from django.db.models import Sum
from compras.models import Compra
from django.utils import timezone

# Create your models here.
class Material(models.Model):#¿Tiene unidad?
    nombre = models.CharField(max_length=100, null=True, blank=False)
    codigo = models.CharField(max_length=10, null=True, blank=False)
    status = models.IntegerField(default=1)
    #Agregar campo de relación unidad-porcion
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    #Obtiene la cantidad en inventario disponible para hacer recetas
    def obtener_cantidad_inventario(self):
        return MaterialInventario.objects.filter(material=self,
            deleted_at__isnull=True, fecha_cad__gte=timezone.now()).aggregate(Sum('cantidad_disponible'))['cantidad_disponible__sum'] or 0

    #Obtiene la cantidad en inventario con mermas
    def obtener_cantidad_inventario_fisico(self):
        return MaterialInventario.objects.filter(material=self,deleted_at__isnull=True).\
            aggregate(Sum('cantidad_disponible'))['cantidad_disponible__sum'] or 0

    def __str__(self):
        return self.nombre

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
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, blank=True, null=True)
    unidad_entrada = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=True, null="True") #se compraron 15 kilos
    porciones = models.IntegerField(blank=True, null="True") #equivale a 20 panqueayudaunidades cambiar porciones
    cantidad_disponible = models.IntegerField(blank=True, null="True") #empieza igual que cantidad
    costo = models.FloatField(blank=True, null="True")
    costo_unitario = models.FloatField(blank=True, null=True)
    fecha_cad = models.DateTimeField(blank=True, null="True")
    estatus = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.material.nombre
