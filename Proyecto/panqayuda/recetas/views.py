from django.shortcuts import render, reverse, redirect, get_object_or_404
# from django.utils import timezone
from .models import Receta
from .forms import RecetaForm, MaterialRecetaForm
# from django.shortcuts import
from django.http import HttpResponse, HttpResponseRedirect

"""
    Función que enlista todas las recetas guardadas dentro de la base de datos.
    Regresa objetos de recetas.
"""
def lista_recetas(request):
    template_name = 'lista_recetas.html'
    recetas = list(Receta.objects.all())
    return render(request, 'recetas/lista_recetas.html', {'recetas': recetas})


def agregar_receta(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.save()
            return redirect('agregar_materiales', id_receta=receta.id)
    else:
        form = RecetaForm()
    return render(request, 'recetas/agregar_receta.html', {'form': form})

def agregar_materiales(request, id_receta):
    receta = get_object_or_404(Receta, pk=id_receta)
    if request.method == "POST":
        form = MaterialRecetaForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.receta = receta
            material.save()
            return render('')
    else:
        form = MaterialRecetaForm()
    return render(request, 'recetas/agregar_materiales.html', {'form': form, 'receta': receta})
