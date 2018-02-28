from django.forms import ModelForm
from django import forms

from .models import Receta, RelacionRecetaMaterial

class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ('nombre', 'cantidad', 'duration')

class RecetaFormManual(forms.Form):
    nombre=forms.CharField(max_length=100, help_text='Nombre de la receta')
    cantidad = forms.IntegerField(help_text='Cantidad de productos que produce')
    duracion = forms.DurationField(help_text='Tiempo de vida del producto')

    def clean(self):
        cleaned_data = super(RecetaForm, self).clean()
        nombre = cleaned_data.get('nombre')
        cantidad = cleaned_data.get('cantidad')
        duration = cleaned_data.get('duracion')
        if not nombre and not cantidad and not duration:
            raise forms.ValidationError('Campos Obligatorios')


class MaterialRecetaForm(ModelForm):
    class Meta:
        model = RelacionRecetaMaterial
        fields = ('material', 'cantidad')
