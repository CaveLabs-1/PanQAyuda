from django.forms import ModelForm
from django import forms
from .models import Proveedor
from django.core.exceptions import ValidationError


class FormaProveedor(ModelForm):
    class Meta:
        model = Proveedor
        fields = ('nombre', 'telefono', 'direccion', 'rfc', 'razon_social', 'email')

    def clean_nombre(self):
        nombre=self.cleaned_data['nombre']

        #Buscar Proveedores que tengan el mismo nombre y que estén disponibles. La consulta no es case-sensitive.
        proveedor_query = Proveedor.objects.filter(nombre__iexact=nombre).exclude(status=0)
        if proveedor_query.count() == 0:
            return nombre
        else:
            if self.instance:
                for proveedor in proveedor_query.all():
                    if proveedor.id == self.instance.id:
                        return nombre
            raise ValidationError("Este proveedor ya existe")
