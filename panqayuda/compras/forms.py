from django.forms import ModelForm
from django import forms
from .models import Compra


class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ('proveedor', 'fecha_compra')
