from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=False)
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El formato del número no es válido.")
    telefono = models.CharField(validators=[telefono_regex], max_length=17, blank=False, null=True)
    direccion = models.CharField(max_length=100, null=True, blank=False)
    rfc = models.CharField(max_length=13, null=True, blank=False)
    razon_social = models.CharField(max_length=100, null=True, blank=False)
    email = models.CharField(max_length=100, null=True, blank=False,
                             validators=[EmailValidator(message='Correo inválido',
                             code=1, whitelist=None)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank = True, null = True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre
