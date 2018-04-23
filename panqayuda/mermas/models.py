from django.db import models
from recetas.models import RecetaInventario
from paquetes.models import PaqueteInventario
from materiales.models import MaterialInventario
from django.utils import timezone

class MermaReceta(models.Model):
    #id receta que se mermó
    nombre = models.ForeignKey(RecetaInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, blank=False)
    fecha = models.DateTimeField(blank=True, null=False)
    descripcion = models.CharField(max_length=500, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.fecha + self.nombre

class MermaPaquete(models.Model):
    #Llave al paquete invenrario del cual se mermo
    nombre = models.ForeignKey(PaqueteInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, blank=False)
    fecha = models.DateTimeField(blank=True, null=False)
    descripcion = models.CharField(max_length=500, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.fecha + self.nombre

class MermaMaterial(models.Model):
    #Llave al modelo del material que se mermo
    nombre = models.ForeignKey(MaterialInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, blank=False)
    fecha = models.DateTimeField(blank=True, null=False)
    descripcion = models.CharField(max_length=500, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.fecha + self.nombre
