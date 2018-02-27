from django.db import models
from django.utils import timezone
from Productos.models import Productos

# Create your models here.
class Paquetes (models.Model):
	nombre = models.CharField(max_length=70)
	producto = models.ManyToManyField(Productos)
	cantidad = models.IntegerField()
	precio = models.FloatField()
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField()

	def _str_(self):
		return self.nombre
