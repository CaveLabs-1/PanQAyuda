from django.forms import ModelForm
from django import forms
from .models import Venta, RelacionVentaPaquete
from django.core.exceptions import ValidationError

class VentaForm(ModelForm):
    class Meta:
        model = Venta
        fields = ('cliente',)

class RelacionVentaPaqueteForm(ModelForm):
    class Meta:
        model = RelacionVentaPaquete
        fields = ('paquete', 'cantidad')
