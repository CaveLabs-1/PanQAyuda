from django.db import models
from django.db.models import Sum, F
from compras.models import Compra
from django.utils import timezone

def unidad_ne():
    return Unidad.objects.get_or_create(nombre = 'N/E')[0]


#Modelo
class Unidad(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Create your models here.
#Modelo de catálogo de materias primas
class Material(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=False)
    codigo = models.CharField(max_length=10, null=True, blank=False)
    status = models.IntegerField(default=1)
    #Agregar campo de relación unidad-porcion
    unidad_entrada = models.ForeignKey(Unidad, on_delete = models.SET(unidad_ne), related_name = 'unidad_entrada')
    unidad_maestra = models.ForeignKey(Unidad, on_delete = models.SET(unidad_ne), related_name = 'unidad_maestra')
    equivale_entrada = models.FloatField(default=1)
    equivale_maestra = models.FloatField(default=1)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    #Obtiene la cantidad en inventario disponible para hacer recetas
    def obtener_cantidad_inventario(self):
        return MaterialInventario.objects.filter(material=self,deleted_at__isnull=True, fecha_cad__gte=timezone.now()).aggregate(Sum('porciones_disponible'))['porciones_disponible__sum'] or 0

    #Obtiene la cantidad en inventario con mermas
    def obtener_cantidad_inventario_fisico(self):
        return MaterialInventario.objects.filter(material=self,deleted_at__isnull=True).\
            aggregate(Sum('porciones_disponible'))['porciones_disponible__sum'] or 0

    #Obtiene los objetos MaterialesInventario con caducados
    def obtener_materiales_inventario_con_caducados(self):
        return MaterialInventario.objects.filter(material=self, deleted_at__isnull=True, porciones_disponible__gt=0)

    #Función que se utiliza cuando se agregan productos terminados al inventario y se utiliza el material de empaque
    def restar_inventario(self,cantidad):
        #Obtener los materiales inventario asociados
        materiales_inventario = MaterialInventario.objects.filter(material=self).filter(deleted_at__isnull=True).order_by('-fecha_cad')
        # Modifica el inventario por recetas, tomando en cuenta la fecha de caducidself.
        for material_inventario in materiales_inventario:
            # Si la cantidad disponible de dicho registro es mayor a la cantidad que se necesita restar,
            # se resta directamente y se termina el proceso.
            if material_inventario.porciones_disponible > cantidad:
                material_inventario.porciones_disponible -= cantidad
                material_inventario.save()
                break

    #Función que se utiliza cuando se eliminan productos terminados y se reeabastece el material de empaque
    def agregar_inventario(self, cantidad):
        materiales_inventario = MaterialInventario.objects.filter(material=self, deleted_at__isnull=True,
                                                                  porciones_disponible__lt=F('porciones')).order_by('-fecha_cad')
        # Abastecer materiales inventario hasta que la cantidad a sumar sea 0
        for material_inventario in materiales_inventario:
            # Este material inventario no puede recibirlo todo
            if cantidad > (material_inventario.porciones - material_inventario.porciones_disponible):
                cantidad -= (material_inventario.porciones - material_inventario.porciones_disponible)
                material_inventario.porciones_disponible = material_inventario.porciones
                material_inventario.save()
            else:
                # Este material inventario puede recibirlo todo
                material_inventario.porciones_disponible += cantidad
                material_inventario.save()
                break

    # Devuelve True si hay materiales inventario caducados, y False en caso contrario
    def tiene_caducados(self):
        # Filtrar: quitar los que están ocupados totalmente y los que están eliminados
        paquetes_inventario = MaterialInventario.objects.filter(material=self, porciones_disponible__gt=0, fecha_cad__lte=timezone.now())
        if paquetes_inventario.count() > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

# Modelo para registros de la materia prima en el inventario.
class MaterialInventario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, blank=True, null=True)
    unidad_entrada = models.ForeignKey(Unidad, on_delete=models.SET(unidad_ne), blank=True, null=True)
    # Cantidad en la unidad en la que se compró.
    cantidad = models.FloatField(blank=True, null=True)
    costo_unitario = models.FloatField(blank=True, null=True)
    # Cantidad en la unidad que se usará en todo el sistema.
    porciones = models.FloatField(blank=True, null=True)
    # Cantidad disponible en la unidad que se usará en todo el sistema.
    porciones_disponible = models.FloatField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    fecha_cad = models.DateTimeField(blank=True, null=True)
    estatus = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.material.nombre + " " + self.fecha_cad.strftime('%d/%m/%Y')

    def es_caducado(self):
        if self.fecha_cad < timezone.now():
            return True
        else:
            return False
