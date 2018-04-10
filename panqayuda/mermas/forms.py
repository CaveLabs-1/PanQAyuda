from django.forms import ModelForm
from django import forms
from .models import MermaPaquete
from .models import MermaMateria

class MermaPaqueteForm(ModelForm):
    class Meta:
        model = MermaPaquete
        fields = (
            'nombre',
            'cantidad',
            'fecha',
            'descripcion'
        )
        widget = {
            'fecha': forms.DateTimeField(),
        }

class MermaMaterialForm(ModelForm):
    class Meta:
        model = MermaMaterial
        fields = (
            'nombre',
            'cantidad',
            'fecha',
            'descripcion'
        )
        widget = {
            'fecha': forms.DateTimeField(),
        }
