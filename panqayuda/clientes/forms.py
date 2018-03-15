from django import forms
from .models import Cliente

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre', 'telefono', 'email', 'rfc')
