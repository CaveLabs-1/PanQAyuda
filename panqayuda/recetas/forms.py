from django.forms import ModelForm
from django import forms
from .models import Receta, RelacionRecetaMaterial
from django.core.exceptions import ValidationError


class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ('nombre', 'cantidad', 'duration')

    def clean_nombre(self):
        nombre=self.cleaned_data['nombre']

        #Buscar recetas que tengan el mismo nombre y que estén disponibles. La consulta no es case-sensitive.
        receta_query = Receta.objects.filter(nombre__iexact=nombre).exclude(status=0)
        if receta_query.count() == 0:
            return nombre
        else:
            raise ValidationError("Esta receta ya existe")


class MaterialRecetaForm(ModelForm):
    class Meta:
        model = RelacionRecetaMaterial
        fields = ('receta','material', 'cantidad')

        error_messages = {
            'cantidad': {
                'required': "Debes seleccionar una cantidad.",
            },
            'material':{
                'required': "Debes seleccionar un material."
            }
        }

    def clean_material(self):
        material = self.cleaned_data['material']
        receta = self.cleaned_data['receta']
        #Buscar si el material ya está en la receta
        material_query = RelacionRecetaMaterial.objects.filter(receta=receta).filter(material=material).exclude(status=0)
        if material_query.count() == 0:
            return material
        else:
            raise ValidationError("El material seleccionado ya está en la receta.")
