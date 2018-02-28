from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import Receta, RelacionRecetaMaterial
from .forms import RecetaForm, MaterialRecetaForm
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.views import generic

"""
    Función que enlista todas las recetas guardadas dentro de la base de datos.
    Regresa objetos de recetas.
"""
def lista_recetas(request):
    template_name = 'lista_recetas.html'
    recetas = list(Receta.objects.filter(status=1))
    return render(request, 'recetas/lista_recetas.html', {'recetas': recetas})


def agregar_receta(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save()
            receta.save()
            # messages.add_message(request, SUCCESS, 'Receta agregada exitosamente.')
            return redirect('agregar_materiales', id_receta=receta.id)
    else:
        form = RecetaForm()
    return render(request, 'recetas/agregar_receta.html', {'form': form})

def detallar_receta(request, id_receta):
    receta_madre = get_object_or_404(Receta, pk=id_receta)
    materiales = list(RelacionRecetaMaterial.objects.filter(receta=receta_madre, status=1))
    print(materiales)
    return render(request, 'recetas/receta.html', {'receta': receta_madre, 'materiales': materiales})

def borrar_receta(request, id_receta):
    receta = get_object_or_404(Receta, pk=id_receta)
    receta.status = 0
    receta.deleted_at = datetime.datetime.now()
    receta.save()
    # messages.add_message(request, SUCCESS, 'Receta borrada exitosamente.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def editar_receta(request, receta):
    receta = get_object_or_404(Receta, pk=receta.id_receta)

# class EditarReceta(UpdateView):
#     model = Receta
#     fields = ['nombre', 'cantidad', 'duration']
#     template_name = 'editar_receta'

    # return render(request, 'editar_receta')

def agregar_materiales(request, id_receta):
    receta_madre = get_object_or_404(Receta, pk=id_receta)
    materiales = list(RelacionRecetaMaterial.objects.filter(receta=receta_madre, status=1))
    if request.method == "POST":
        form = MaterialRecetaForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.receta = receta_madre
            material.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = MaterialRecetaForm()
    print(materiales)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'recetas/agregar_materiales.html', {'form': form, 'receta': receta_madre, 'materiales': materiales})

def borrar_material(request, id_material):
    material = get_object_or_404(RelacionRecetaMaterial, pk=id_material)
    id_receta=material.receta.id
    material.status = 0
    material.save()
    # messages.add_message(request, SUCCESS, 'Receta borrada exitosamente.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
