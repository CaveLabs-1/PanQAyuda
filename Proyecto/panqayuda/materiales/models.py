from django.db import models
from django.utils import timezone

# Create your models here.
class Material(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=False)
    unidad = models.CharField(max_length=10, null=True, blank=False)
    codigo = models.CharField(max_length=10, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

