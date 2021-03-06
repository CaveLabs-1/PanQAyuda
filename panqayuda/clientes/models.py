from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Cliente(models.Model):
    class Meta:
        ordering = ['nombre']

    nombre = models.CharField(max_length=100, null = True)
    nombreContacto = models.CharField(max_length=100, null = True, default='David')
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El formato del número no es válido.")
    telefono = models.CharField(validators=[telefono_regex], max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=70,blank=True, null=True)
    rfc = models.CharField(max_length=13, blank = True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre
