from django import template
from django.contrib.auth.models import Group

register = template.Library()

#Ve si el usuario pertenece a cierto grupo
@register.filter(name='tiene_grupo')
def tiene_grupo(usuario, nombre_grupo):
    grupo =  Group.objects.get(name=nombre_grupo)
    return grupo in usuario.groups.all()