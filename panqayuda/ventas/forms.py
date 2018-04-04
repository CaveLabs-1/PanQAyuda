from django.forms import ModelForm
from django import forms
from .models import Venta
from django.core.exceptions import ValidationError

class VentaForm(ModelForm):
    class Meta:
        model = Venta
        fields = ('cliente', 'monto')
