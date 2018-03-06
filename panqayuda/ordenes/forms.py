from django import forms
from .models import Orden

class FormOrden(forms.ModelForm):
     class Meta:
          model = Orden
          fields = ('receta', 'multiplicador', 'fecha_fin')
