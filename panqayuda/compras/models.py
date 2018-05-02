from django.db import models
from django.utils import timezone
from proveedores.models import Proveedor
from django.core.validators import MinValueValidator

class Compra(models.Model):
    #Llave foranea al modelo de proveedor ya que una compra siempre esta cinculada al proveedor que te vende
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.proveedor.nombre
