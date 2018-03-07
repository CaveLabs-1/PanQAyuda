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
                print("2")
                for paquete in paquete_existente.all():
                    if paquete.id==self.instance.id:
                        print("3")
                        return nombre
            raise ValidationError('Ya hay un paquete con este nombre')
    class Meta:
        model = Paquete
        fields = ('nombre', 'precio')

    

class FormRecetasPorPaquete(forms.ModelForm):
    class Meta:
        model = RecetasPorPaquete
        fields = ('receta', 'cantidad', 'paquete')

class FormPaqueteInventario(forms.ModelForm):
    class Meta:
        model = PaqueteInventario
        fields = ('nombre', 'cantidad', 'fecha_cad')
