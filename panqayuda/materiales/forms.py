from django.forms import ModelForm
from django import forms
from .models import Material
from django.core.exceptions import ValidationError


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ('nombre', 'unidad', 'codigo')

    def clean_nombre(self):
        nombre=self.cleaned_data['nombre']

        #Buscar materials que tengan el mismo nombre y que estén disponibles. La consulta no es case-sensitive.
        material_query = Material.objects.filter(nombre__iexact=nombre).exclude(status=0)
        if material_query.count() == 0:
            return nombre
        else:
            if self.instance:
                for material in material_query.all():
                    if material.id == self.instance.id:
                        return nombre
            raise ValidationError("Este material ya existe")
