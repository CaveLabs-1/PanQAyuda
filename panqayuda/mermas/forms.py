from django.forms import ModelForm
from django import forms
from .models import MermaPaquete

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
