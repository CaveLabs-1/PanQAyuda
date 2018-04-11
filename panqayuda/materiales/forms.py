from django.forms import ModelForm
from django import forms
from .models import Material, Unidad, MaterialInventario
from django.core.exceptions import ValidationError


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ('nombre', 'codigo')

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

class UnidadForm(ModelForm):
    class Meta:
        model = Unidad
        fields = ('nombre', )
        error_messages = {
            'nombre': {
                'required': "Este campo no puede ser vacío",
            },
        }

    def clean_nombre(self):
        nombre=self.cleaned_data['nombre']
        unidad_existente=Unidad.objects.filter(deleted_at__isnull= True).filter(nombre__iexact=nombre)
        if unidad_existente.count() == 0:
            return nombre
        else: # si ya existe uno con ese nombre
            if self.instance:
                for unidad in unidad_existente.all():
                    if unidad.id==self.instance.id:
                        return nombre
            raise ValidationError('Ya hay una unidad con este nombre')

class MaterialInventarioForm(ModelForm):
    class Meta:
        model = MaterialInventario
        fields = ('material', 'compra', 'unidad_entrada', 'cantidad', 'porciones', 'costo', 'fecha_cad' )
