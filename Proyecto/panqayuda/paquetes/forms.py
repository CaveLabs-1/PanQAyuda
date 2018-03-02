from django import forms
from .models import Paquete
from .models import Recetas_por_paquete, Paquete_Inventario
from recetas.models import Receta

class FormPaquete(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ('nombre', 'precio')

class FormRecetasPorPaquete(forms.ModelForm):
    class Meta:
        model = Recetas_por_paquete
        fields = ('receta', 'cantidad', 'paquete')

class FormPaqueteInventario(forms.ModelForm):
    class Meta:
        model = Paquete_Inventario
        fields = ('nombre', 'cantidad', 'fecha_cad')
