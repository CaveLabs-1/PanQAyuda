from django.forms import ModelForm
from django import forms
from .models import Receta, RelacionRecetaMaterial
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class RecetaForm(ModelForm):
    #Campo que se transformará en un timedelta
    duracion_en_dias = forms.IntegerField(validators=[MinValueValidator(1, "La duración en días debe ser un número entero mayor a 0.")], required=True)

    class Meta:
        model = Receta
        fields = ('nombre', 'codigo', 'cantidad', 'duracion_en_dias')

    def clean_nombre(self):
        nombre=self.cleaned_data['nombre']

        #Buscar recetas que tengan el mismo nombre y que estén disponibles. La consulta no es case-sensitive.
        receta_query = Receta.objects.filter(nombre__iexact=nombre).exclude(status=0)
        if receta_query.count() == 0:
            return nombre
        else:
            if self.instance:
                for receta in receta_query.all():
                    if receta.id == self.instance.id:
                        return nombre
            raise ValidationError("Este producto semiterminado ya existe")

class MaterialRecetaForm(ModelForm):
    class Meta:
        model = RelacionRecetaMaterial
        fields = ('receta','material', 'cantidad')

        error_messages = {
            'cantidad': {
                'required': "Debes seleccionar una cantidad.",
            },
            'material':{
                'required': "Debes seleccionar una materia prima."
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
            raise ValidationError("La materia prima seleccionada ya está en la receta del producto semiterminado.")
