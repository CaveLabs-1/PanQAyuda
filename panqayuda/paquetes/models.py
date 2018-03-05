from django.db import models
from django.utils import timezone
from recetas.models import Receta

# Create your models here.
class Paquete (models.Model):
	nombre = models.CharField(max_length=70)
	recetas = models.ManyToManyField(Receta, through='Recetas_por_paquete', through_fields=('paquete', 'receta'),)
	precio = models.FloatField()
	estatus = models.IntegerField(default=1)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(blank=True, null=True)

	def _str_(self):
		return self.nombre


class Recetas_por_paquete (models.Model):
	paquete=models.ForeignKey(Paquete, on_delete=models.CASCADE)
	receta=models.ForeignKey(Receta, on_delete=models.CASCADE)
	cantidad=models.IntegerField(default=1)

	def recetas_paquete(paquete):
		return Recetas_por_paquete.objects.filter(paquete=paquete)


class Paquete_Inventario (models.Model):
	nombre= models.ForeignKey(Paquete, on_delete=models.CASCADE)
	cantidad= models.IntegerField()
	fecha_cad = models.DateTimeField(blank = True, null = True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(blank = True, null = True)
