from django.shortcuts import render,reverse,redirect
from .forms import MaterialForm, UnidadForm
from .models import Material
from django.contrib import messages
from django.http import HttpResponseRedirect
from panqayuda.decorators import group_required
import datetime


# Create your views here.

def materiales(request):
    if request.method == 'POST':
        forma_post = MaterialForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado un nuevo material.')
        else:
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')

        return HttpResponseRedirect(reverse('materiales:materiales'))
    else:
        forma = MaterialForm()
        materiales =  Material.objects.filter(deleted_at__isnull=True)
        return render (request, 'materiales/materiales.html', {'forma': forma, 'materiales': materiales})



"""
    View que está haciendo Rudy
"""
@group_required('admin')
def lista_unidades(request):
    return render(request, 'materiales/lista_unidades.html')

"""
    Función que agrega una nueva unidad a la base de datos según la forma, si no tiene
    un POST te regresa la forma para hacerlo
"""
@group_required('admin')
def agregar_unidades(request):
    if request.method == "POST":
        form = UnidadForm(request.POST)
        if form.is_valid():
             unidad = form.save()
             unidad.save()
             messages.success(request, '¡Se ha agregado la unidad al catálogo!')
             return redirect('/materiales/lista_unidades')
        else:
             messages.success(request, '¡Ya hay una unidad con este nombre!')
             return redirect('/materiales/lista_unidades')
    else:
        messages.success(request, '¡Hubo un error con el POST!')
        return redirect('/materiales/lista_unidades')
