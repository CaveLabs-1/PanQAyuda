from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from django.core.validators import MinValueValidator

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    paquetes = models.ManyToManyField('paquetes.PaqueteInventario', through = 'RelacionVentaPaquete')
    monto = models.IntegerField(default=0, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.cliente + self.created_at

class RelacionVentaPaquete(models.Model):
    venta = models.ForeignKey('Venta', on_delete = models.CASCADE)
    paquete = models.ForeignKey('paquetes.PaqueteInventario',  on_delete = models.CASCADE)
    cantidad = models.DecimalField(null=True, blank=False,max_digits=10, decimal_places=5,
                                   validators=[MinValueValidator(0.000001, "Debes seleccionar una cantidad mayor a 0.")])
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.receta.nombre
