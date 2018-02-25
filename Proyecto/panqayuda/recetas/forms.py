from django.forms import ModelForm

from .models import Receta

class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ('nombre', 'cantidad', 'duration', 'material')
