from django.db import models
from django.db.models import Sum
from compras.models import Compra
from django.utils import timezone

def get_unidad_eliminada():
    return Unidad.objects.get_or_create(nombre = 'N/E')[0]

# Create your models here.
class Material(models.Model):#¿Tiene unidad?
    nombre = models.CharField(max_length=100, null=True, blank=False)
    codigo = models.CharField(max_length=10, null=True, blank=False)
    status = models.IntegerField(default=1)
    #Agregar campo de relación unidad-porcion
    unidad_entrada = models.ForeignKey(Unidad, on_delete = models.SET(get_unidad_eliminada))
    unidad_maestra = models.ForeignKey(Unidad, on_delete = models.SET(get_unidad_eliminada))
    equivale_entrada = models.FloatField(null=False, blank=False)
    equivale_maestra = models.FloatField(null=False, blank=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)


    def obtener_cantidad_inventario(self):
        return MaterialInventario.objects.filter(material=self,
            deleted_at__isnull=True, fecha_cad__gte=timezone.now()).aggregate(Sum('cantidad_disponible'))['cantidad_disponible__sum'] or 0

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

# Modelo para registros de la materia prima en el inventario.
class MaterialInventario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, blank=True, null=True)
    unidad_entrada = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True)
    # Cantidad en la unidad en la que se compró.
    cantidad = models.FloatField(blank=True, null=True)
    # Cantidad en la unidad que se usará en todo el sistema.
    porciones = models.FloatField(blank=True, null=True)
    # Cantidad disponible en la unidad que se usará en todo el sistema.
    porciones_disponible = models.FloatField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    fecha_cad = models.DateTimeField(blank=True, null=True)
    estatus = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.material.nombre
