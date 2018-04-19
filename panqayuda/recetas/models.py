from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import datetime
from django.db.models import Sum, F

class Receta(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=False)
    cantidad = models.IntegerField(null=True, blank=False, validators=[MinValueValidator(1, "Debes seleccionar un número entero mayor a 0.")])
    duration = models.DurationField(null=True, blank=False)
    material = models.ManyToManyField('materiales.Material', through = 'RelacionRecetaMaterial')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre

    #Para agregar o quitar paquetes
    def obtener_cantidad_inventario(self):
        return RecetaInventario.objects.filter(nombre=self).filter(deleted_at__isnull=True). \
                   filter(fecha_cad__gte=datetime.datetime.now()).filter(cantidad__gt=0). \
                   annotate(disponible=Sum(F('cantidad') - F('ocupados'))). \
                   aggregate(porciones_disponible=Sum('disponible'))['porciones_disponible'] or -1

    #Para el detalle de las recetas inventario
    def obtener_cantidad_inventario_con_caducados(self):
        return RecetaInventario.objects.filter(nombre=self).filter(deleted_at__isnull=True). \
                   filter(cantidad__gt=0). \
                   annotate(disponible=Sum(F('cantidad') - F('ocupados'))). \
                   aggregate(porciones_disponible=Sum('disponible'))['porciones_disponible'] or 0

    #Devuelve True si hay paquetes caducados, y False en caso contrario
    def tiene_caducados(self):
        #Filtrar: quitar los que están ocupados totalmente y los que están eliminados
        recetas_inventario = self.obtener_recetas_inventario().filter(fecha_cad__gte=datetime.datetime.now())
        if recetas_inventario.count() > 0:
            return True
        else:
            return False

    #Obtener las recetas inventrio de cierta receta
    def obtener_recetas_inventario(self):
        return RecetaInventario.objects.annotate(disponibles=Sum(F('cantidad')-F('ocupados')))\
            .filter(nombre_id=self, deleted_at__isnull=True, disponibles__gt=0)

    def obtener_recetas_inventario_con_caducados(self):
        return RecetaInventario.objects.annotate(disponibles=Sum(F('cantidad') - F('ocupados'))) \
            .filter(nombre_id=self, deleted_at__isnull=True, disponibles__gt=0).order_by('fecha_cad')

class RelacionRecetaMaterial(models.Model):
    receta = models.ForeignKey('Receta', on_delete = models.CASCADE)
    material = models.ForeignKey('materiales.Material',  on_delete = models.CASCADE)
    cantidad = models.DecimalField(null=True, blank=False,max_digits=10, decimal_places=5,
                                   validators=[MinValueValidator(0.000001, "Debes seleccionar una cantidad mayor a 0.")])
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.receta.nombre

class RecetaInventario(models.Model):
    nombre = models.ForeignKey('Receta', on_delete = models.CASCADE)
    cantidad = models.IntegerField(null=True, blank=False, validators=[MinValueValidator(1, "Debes seleccionar un número entero mator a 0.")])
    ocupados = models.IntegerField(default=0, blank=True, null=False)
    fecha_cad = models.DateTimeField(blank = True, null = True)
    estatus = models.IntegerField(default=1)
    costo = models.FloatField(blank=True, null="True")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.nombre.nombre + " " + self.fecha_cad.strftime("%d/%m/%Y")

    def obtener_cantidad_inventario(receta):
            return RecetaInventario.objects.filter(nombre=receta).filter(deleted_at__isnull=True).\
            filter(fecha_cad__gte=datetime.datetime.now()).filter(cantidad__gt=0).\
            annotate(disponible=Sum(F('cantidad')-F('ocupados'))).\
            aggregate(porciones_disponible=Sum('disponible'))['porciones_disponible'] or -1

    def obtener_disponibles(receta):
        return RecetaInventario.objects.filter(nombre=receta).filter(deleted_at__isnull=True).\
        filter(fecha_cad__gte=datetime.datetime.now()).annotate(disponible=Sum(F('cantidad')-F('ocupados'))).\
        filter(disponible__gt=0).order_by('fecha_cad')

    def es_caducado(self):
        if self.fecha_cad < timezone.now():
            return True
        else:
            return False

    def disponibles(self):
        return self.cantidad - self.ocupados

