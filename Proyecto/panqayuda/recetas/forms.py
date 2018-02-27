from django.forms import ModelForm

from .models import Receta, RelacionRecetaMaterial

class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ('nombre', 'cantidad', 'duration')

class MaterialRecetaForm(ModelForm):
    class Meta:
        model = RelacionRecetaMaterial
        fields = ('material', 'cantidad')
