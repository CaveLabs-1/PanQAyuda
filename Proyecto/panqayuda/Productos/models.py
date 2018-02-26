from django.db import models
from django.utils import timezone

class Productos (models.Model):
	nombre = models.CharField(max_length=50)
	cantidad = models.IntegerField()
	costo = models.FloatField()
	caducidad = models.DateTimeField(default=timezone.now)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(default=timezone.now)

	def _str_(self):
		return self.nombre
