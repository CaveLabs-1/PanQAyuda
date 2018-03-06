from django.db import models
from django.utils import timezone
from recetas.models import Receta

class Orden(models.Model):

    LISTA_ESTATUS = (
        ('0', 'Cancelada'),
        ('1', 'Por Trabajar'),
        ('2', 'Listo'),
    )

    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    multiplicador = models.IntegerField()
    estatus = models.CharField(default='1' , max_length = 1, choices=LISTA_ESTATUS)
    fecha_fin = models.DateTimeField(blank = True, null = True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)

    def ordenes_por_entregar():
        return Orden.objects.filter(estatus = '1')

    def ordenes_lsitas():
        return Orden.objects.filter(estatus = '2')

    def cantidad():
        return self.receta.cantidad * self.multiplicador


    def _str_(self):
        cantidad = str(self.receta.cantidad * self.multiplicador)
        return self.cantidad + self.receta.nombre
