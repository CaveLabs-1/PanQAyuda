from django.db import models
from django.utils import timezone
from recetas.models import Receta
from django.core.validators import MinValueValidator

# Create your models here.
class Paquete (models.Model):
	nombre = models.CharField(max_length=70)
	recetas = models.ManyToManyField(Receta, through='RecetasPorPaquete', through_fields=('paquete', 'receta'),)
	precio = models.FloatField(validators=[MinValueValidator(0.00001, "El precio del paquete debe ser mayor a 0.")])
	estatus = models.IntegerField(default=1)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(blank=True, null=True)
	def __str__(self):
		return self.nombre


class RecetasPorPaquete (models.Model):
	paquete=models.ForeignKey(Paquete, on_delete=models.CASCADE)
	receta=models.ForeignKey(Receta, on_delete=models.CASCADE)
	cantidad=models.IntegerField(default=1, blank=False,validators=[MinValueValidator(1,"Debes seleccionar un número entero mayor a 0.") ])
	estatus = models.IntegerField(default=1)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(blank=True, null=True)

	def recetas_paquete(paquete):
		return RecetasPorPaquete.objects.filter(paquete=paquete)
	def __str__(self):
		return self.paquete.nombre

class PaqueteInventario (models.Model):
	nombre= models.ForeignKey(Paquete, on_delete=models.CASCADE)
	cantidad= models.IntegerField(validators=[MinValueValidator(1, "Debes seleccionar un número entero mayor a 0.")])
	fecha_cad = models.DateTimeField(blank = True, null = True)
	estatus = models.IntegerField(default=1)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(blank = True, null = True)

	def __str__(self):
		return self.nombre.nombre
