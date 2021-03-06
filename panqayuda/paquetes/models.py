from django.db import models
from django.db.models import Sum, F
import datetime
from django.utils import timezone
from recetas.models import Receta
from django.core.validators import MinValueValidator

# Create your models here.
class Paquete (models.Model):

	nombre = models.CharField(max_length=70)
	codigo = models.CharField(max_length=10, null=True, blank=False)
	recetas = models.ManyToManyField(Receta, through='RecetasPorPaquete', through_fields=('paquete', 'receta'),)
	precio = models.FloatField(validators=[MinValueValidator(0.00001, "El precio del paquete debe ser mayor a 0.")])
	estatus = models.IntegerField(default=1)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(blank=True, null=True)

	#Devuelve el nombre del paquete
	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


	#Devuelve el número de paquetes en inventario disponibles para este tipo de paquete
	def obtener_disponibles_inventario(self):
		return PaqueteInventario.objects.filter(nombre=self).filter(deleted_at__isnull=True).\
			filter(fecha_cad__gte=timezone.now()).annotate(disponible=Sum(F('cantidad')- F('ocupados'))).\
			aggregate(porciones_disponible=Sum('disponible'))['porciones_disponible'] or 0

	#Devuelve el número de paquetes incluyendo las mermas
	def obtener_inventario_fisico(self):
		return PaqueteInventario.objects.filter(nombre=self).filter(deleted_at__isnull=True).\
				   annotate(disponible=Sum(F('cantidad') - F('ocupados'))).\
				   aggregate(porciones_disponible=Sum('disponible'))['porciones_disponible'] or 0

	#Devuelve la lista de paquetes_inventario que tienen paquetes disponibles
	def obtener_paquetes_inventario_disponibles(self):
		return PaqueteInventario.objects.filter(nombre=self).filter(deleted_at__isnull=True). \
			filter(fecha_cad__gte=timezone.now()).annotate(disponible=Sum(F('cantidad') - F('ocupados'))). \
			filter(disponible__gt=0).order_by('fecha_cad')

#-----------------------------------------------------------------
	#Devuelve la lista de paquetes_inventario que tienen algun paquete ocupado
	def obtener_paquetes_inventario_ocupado(self):
		return PaqueteInventario.objects.filter(nombre=self).filter(deleted_at__isnull=True). \
			filter(fecha_cad__gte=timezone.now()). \
			exclude(ocupados=0).order_by('fecha_cad')

#-----------------------------------------------------------------

	#Devuelve los paquetes en inventario incluyendo a los que ya pasó su fecha de caducidad
	def obtener_paquetes_inventario_con_caducados(self):
		return PaqueteInventario.objects.filter(nombre=self).filter(deleted_at__isnull=True). \
			annotate(disponible=Sum(F('cantidad') - F('ocupados'))).filter(disponible__gte=0).order_by('fecha_cad')

	# Devuelve True si hay paquetes caducados, y False en caso contrario
	def tiene_caducados(self):
		# Filtrar: quitar los que están ocupados totalmente y los que están eliminados
		paquetes_inventario = self.obtener_paquetes_inventario_con_caducados().exclude(fecha_cad__gte=timezone.now())
		if paquetes_inventario.count() > 0:
			return True
		else:
			return False

class RecetasPorPaquete (models.Model):
	paquete=models.ForeignKey(Paquete, on_delete=models.CASCADE)
	receta=models.ForeignKey(Receta, on_delete=models.CASCADE)
	cantidad=models.FloatField(default=1, blank=False,validators=[MinValueValidator(0.1,"Debes seleccionar un número mayor a 0.") ])
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
	ocupados = models.IntegerField(default=0, blank=True, null=False)
	fecha_cad = models.DateTimeField(blank = True, null = True)
	costo = models.FloatField(blank=True, null="True")
	estatus = models.IntegerField(default=1)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	deleted_at = models.DateTimeField(blank = True, null = True)

	#Regresa el nombre del paquete en inventario
	def __str__(self):
		return self.nombre.nombre + " " + self.fecha_cad.strftime("%d/%m/%Y")

	#Devuelve la resta entre la cantidad y los ocupados
	def disponibles(self):
		return self.cantidad - self.ocupados

	def multiplicar_costo_cantidad(self):
		return self.cantidad * self.costo

	def es_caducado(self):
		if self.fecha_cad < timezone.now():
			return True
		else:
			return False
