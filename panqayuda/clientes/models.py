from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null = False)
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El formato del número no es válido.")
    telefono = models.CharField(validators=[telefono_regex], max_length=17, blank=True)
    email = models.EmailField(max_length=70,blank=True)
    rfc = models.CharField(max_length=13, blank = True)

    def __str__(self):
        return self.nombre
