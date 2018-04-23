from django import forms
from .models import Paquete
from .models import RecetasPorPaquete, PaqueteInventario
from recetas.models import Receta
from django.core.exceptions import ValidationError

class FormPaquete(forms.ModelForm):
    def clean_nombre(self):
        nombre=self.cleaned_data['nombre']
        paquete_existente=Paquete.objects.filter(deleted_at__isnull= True).filter(nombre__iexact=nombre)
        if paquete_existente.count() == 0:
            return nombre
        else:
            if self.instance:
                for paquete in paquete_existente.all():
                    if paquete.id==self.instance.id:
                        return nombre
            raise ValidationError('Ya hay un paquete con este nombre')
    class Meta:
        model = Paquete
        fields = ('nombre', 'precio')

        error_messages = {
            'nombre':{
                'required':"Este campo no puede ser vacio",
            },
            'precio':{
                'required':"Este campo no puede ser vacio",
            },
        }

class FormEditarPaquete (forms.ModelForm):
    class Meta:
        model = PaqueteInventario
        fields = ('cantidad', 'fecha_cad')

        error_messages = {
            'cantidad': {
                'required': "Debes seleccionar una cantidad mayor a 0.",
            },
            'fecha_cad':{
                'required': "Debes seleccionar una fecha",
            }
        }

class FormRecetasPorPaquete(forms.ModelForm):
    class Meta:
        model = RecetasPorPaquete
        fields = ('receta', 'cantidad', 'paquete')

        error_messages = {
            'cantidad': {
                'required': "Debes seleccionar una cantidad mayor a 0.",
            },
            'receta': {
                'required': "Debes seleccionar una receta",
                'invalid_choice': "Debes seleccionar una receta",
            }
        }

class FormPaqueteInventario(forms.ModelForm):
    class Meta:
        model = PaqueteInventario
        fields = ('nombre', 'cantidad', 'fecha_cad')

        error_messages = {
            'nombre': {
                'required': "Debes seleccionar un paquete.",
            },
            'cantidad': {
                'required': "Debes seleccionar una cantidad mayor a 0.",
            },
            'fecha_cad': {
                'required': "Debes seleccionar una fecha",
            }
        }
