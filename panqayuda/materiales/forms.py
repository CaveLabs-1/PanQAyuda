from django.forms import ModelForm
from django import forms
from .models import Material, Unidad, MaterialInventario
from django.core.exceptions import ValidationError


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ('nombre', 'codigo', 'unidad_entrada', 'unidad_maestra', 'equivale_entrada', 'equivale_maestra')

    def clean_nombre(self):
        nombre=self.cleaned_data['nombre']

        #Buscar materials que tengan el mismo nombre y que estén disponibles. La consulta no es case-sensitive.
        material_query = Material.objects.filter(nombre__iexact=nombre).exclude(status=0).exclude(deleted_at__isnull=False)
        if material_query.count() == 0:
            return nombre
        else:
            if self.instance:
                for material in material_query.all():
                    if material.id == self.instance.id:
                        return nombre
            raise ValidationError("Este material ya existe")

#Forma con el campo único de nombre para unidades
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
        fields = ('material', 'compra', 'cantidad', 'costo', 'fecha_cad')

    def clean_cantidad(self):
        cantidad=self.cleaned_data['cantidad']
        if cantidad > 0:
            return cantidad
        else:
            raise ValidationError("La cantidad debe ser mayor a 0.")
