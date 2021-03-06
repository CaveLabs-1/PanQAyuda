from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from django.core.validators import MinValueValidator
from paquetes.models import Paquete

class Venta(models.Model):
    #Llave foranea al modelo de cliente ya que una venta siempre esta atada a un comprador
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto_total = models.DecimalField(null=True, blank=False,max_digits=10, decimal_places=5)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.cliente.nombre + " - " + self.created_at.strftime("%d/%m/%Y")

class RelacionVentaPaquete(models.Model):
    #Llave al modelo de venta y a paquete para relacionar los paquetes que se vendieron en una sola venta
    venta = models.ForeignKey(Venta, on_delete = models.CASCADE)
    paquete = models.ForeignKey(Paquete,  on_delete = models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=True,validators=[MinValueValidator(1, "Debes seleccionar una cantidad mayor a 0.")])
    status = models.IntegerField(default=1)
    monto = models.DecimalField(null=True, blank=False,max_digits=10, decimal_places=5,
                                   validators=[MinValueValidator(0.000001, "Debes seleccionar una cantidad mayor a 0.")])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.paquete.nombre

    def precio_unitario(self):
        return self.monto/self.cantidad
