from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class FormUser(forms.ModelForm):
    #Revisar que no exista otro usuario con el mismo username
    def clean_username(self):
        username=self.cleaned_data['username']
        usuario_existente=User.objects.filter(is_active=1).filter(username__iexact=username)
        if usuario_existente.count() == 0:
            return username
        else:
            if self.instance:
                for usuario in usuario_existente.all():
                    if usuario.id==self.instance.id: #checar que el que se encontró con el mismo username sea el que se está modificando
                        return username
            raise ValidationError('Ya hay un usuario con este nombre usuario', code='invalid')

    #Revisar que no exista otro usuario con el mismo email
    def clean_email(self):
        email=self.cleaned_data['email']
        email_existente=User.objects.filter(is_active=1).filter(email__iexact=email)
        if email_existente.count() == 0:
            return email
        else:
            if self.instance:
                for email in email_existente.all():
                    if email.id==self.instance.id:#checar que el que se encontró con el mismo correo sea el que se está modificando
                        return email
            raise ValidationError('Ya hay un usuario con este correo', code='invalid')
    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff')
