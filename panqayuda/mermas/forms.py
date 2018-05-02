from django.forms import ModelForm
from django import forms
from .models import MermaPaquete
from .models import MermaMaterial
from .models import MermaReceta


class MermaPaqueteForm(ModelForm):
    class Meta:
        model = MermaPaquete
        fields = (
            'nombre',
            'cantidad',
            'descripcion'
        )

class MermaMaterialForm(ModelForm):
    class Meta:
        model = MermaMaterial
        fields = (
            'nombre',
            'cantidad',
            'descripcion'
        )

class MermaRecetaForm(ModelForm):
    class Meta:
        model = MermaReceta
        fields = (
            'nombre',
            'cantidad',
            'descripcion'
        )