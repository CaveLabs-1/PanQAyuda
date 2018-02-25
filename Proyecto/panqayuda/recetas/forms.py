from django.forms import ModelForm

from panqayuda.models import Receta

class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ('nombre', 'cantidad', 'duracion', 'material')
