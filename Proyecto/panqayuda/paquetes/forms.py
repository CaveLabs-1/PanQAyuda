from django import forms
from .models import Paquete
from .models import Recetas_por_paquete
from recetas.models import Receta

class FormPaquete(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ('nombre', 'precio', 'created_at', 'updated_at', 'deleted_at')

class FormRecetasPorPaquete(forms.ModelForm):
    class Meta:
        model = Recetas_por_paquete 
        fields = ('receta', 'cantidad', 'paquete')
