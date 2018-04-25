from django.db import models
from django.utils import timezone
from recetas.models import Receta
from django.core.exceptions import ValidationError
import datetime

def validate_fecha_mayor_fecha_actual(value):
    if value < datetime.date.today():
        raise ValidationError('La fecha no puede ser menor a la fecha actual.')

def validate_no_multiplicadores_menores_a_0(value):
    if value < 0:
        raise ValidationError('EL multiplicador no puede ser menor a 0')

class Orden(models.Model):

    LISTA_ESTATUS = (
        ('0', 'Cancelada'),
        ('1', 'Por Trabajar'),
        ('2', 'Listo'),
    )

    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    multiplicador = models.IntegerField(validators=[validate_no_multiplicadores_menores_a_0])
    estatus = models.CharField(default='1' , max_length = 1, choices=LISTA_ESTATUS)
    fecha_fin = models.DateField(blank = True, null = True, validators=[validate_fecha_mayor_fecha_actual])
    costo = models.FloatField(blank=True, null="True")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)

    def ordenes_por_entregar():
        return Orden.objects.filter(estatus='1')

    def ordenes_lsitas():
        return Orden.objects.filter(estatus='2')

    def cantidad(self):
        return self.receta.cantidad * self.multiplicador

    def _str_(self):
        cantidad = str(self.receta.cantidad * self.multiplicador)
        return self.cantidad + self.receta.nombre




class Estatus_Orden(models.Model):
    estatus = models.CharField(max_length=15)
