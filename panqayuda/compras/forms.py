from django.forms import ModelForm
from django import forms
from .models import Compra
from django.core.exceptions import ValidationError

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ('proveedor',)
