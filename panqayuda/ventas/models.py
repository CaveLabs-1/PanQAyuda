from django.db import models
from django.utils import timezone
from clientes.models import Cliente

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.IntegerField(default=0, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.cliente + self.created_at
