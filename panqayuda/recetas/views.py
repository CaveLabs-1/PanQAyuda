from django.shortcuts import render, redirect, get_object_or_404
from .models import Receta, RelacionRecetaMaterial
from django.contrib import messages
from materiales.models import Material
from .forms import RecetaForm, MaterialRecetaForm
from django.http import HttpResponse, HttpResponseRedirect
import datetime
# from django.contrib import messages
# from django.views.generic.edit import UpdateView
# from django.views import generic

"""
    Función que enlista todas las recetas guardadas dentro de la base de datos.
    Regresa objetos de recetas.
"""


def lista_recetas(request):
    template_name = 'lista_recetas.html'
    recetas = list(Receta.objects.filter(status=1))
    return render(request, 'recetas/lista_recetas.html', {'recetas': recetas})


"""
    Función que agrega una receta a la base de datos según la forma, si no tiene
    un POST te regresa la forms para hacerlo
"""


def agregar_receta(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save()
            receta.save()
            messages.success(request, 'Se ha agregado la receta al catálogo!')
            return redirect('recetas:agregar_materiales', id_receta=receta.id)
    else:
        form = RecetaForm()
    return render(request, 'recetas/agregar_receta.html', {'form': form})


"""
    Muestra toda la información de la receta incluyendo los materiales que tiene asignados
"""

def detallar_receta(request, id_receta):
    receta_madre = get_object_or_404(Receta, pk=id_receta)
    materiales = list(RelacionRecetaMaterial.objects.filter(receta=receta_madre, status=1))
    return render(request, 'recetas/receta.html', {'receta': receta_madre, 'materiales': materiales})


"""
    Recibe el id de la receta a borrar, cambia el estatus de esta a 0 y agrega la fecha de
    borrado a la celda correspondiente

    0 significa que la receta fue borrada
"""


def borrar_receta(request, id_receta):
    receta = get_object_or_404(Receta, pk=id_receta)
    receta.status = 0
    receta.deleted_at = datetime.datetime.now()
    receta.save()
    messages.success(request, 'Se ha borrado la receta exitosamente!')
    # messages.add_message(request, SUCCESS, 'Receta borrada exitosamente.')
    # recetas = list(Receta.objects.filter(status=1))
    return redirect('recetas:lista_de_recetas')
    # return render(request, 'recetas/lista_recetas.html', {'recetas': recetas})


"""
    Recibe el id de la receta a cambiarse, en caso de post cambia los datos de la recetas
    a cambiar, en caso de get regresa la forma con los datos a cambiar
"""


def editar_receta(request, id_receta):
    receta = get_object_or_404(Receta, pk=id_receta)
    if request.method == "POST":
        form = RecetaForm(request.POST or None, instance=receta)
        if form.is_valid():
            receta = form.save()
            receta.save
            messages.success(request, 'Se ha editado la receta exitosamente!')
            materiales = list(RelacionRecetaMaterial.objects.filter(receta=receta, status=1))
            return render(request, 'recetas/receta.html', {'receta': receta, 'materiales': materiales})
    else:
        form = RecetaForm()
    return render(request, 'recetas/editar_receta.html', {'form': form, 'receta': receta})


"""
    Recibe el id de la receta a la cual se le van a agregar los materiales junto con el objetos
    de material que va a ser agregado a la receta
"""


def agregar_materiales(request, id_receta):
    receta = get_object_or_404(Receta, pk=id_receta)
    # Los materiales que aún no se han agregado a la receta
    aux = RelacionRecetaMaterial.objects.filter(receta=4).exclude(status=0)
    materiales_disponibles = Material.objects.exclude(id__in=aux)

    materiales_actuales = RelacionRecetaMaterial.objects.filter(receta=receta).exclude(status=0)
    if request.method == "POST":
        data = {'material': Material.objects.get(nombre=request.POST['material']).id, 'cantidad': request.POST['cantidad']}
        form = MaterialRecetaForm(data)
        if form.is_valid():
            material = form.save(commit=False)
            material.receta = receta
            material.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = MaterialRecetaForm()
    return render(request, 'recetas/agregar_materiales.html', {'form': form, 'receta': receta, 'materiales_actuales': materiales_actuales, 'materiales_disponibles': materiales_disponibles })


"""
    Recibe el id de el material a borrar, cambia el status de dicho material a 0 y agrega
    la fecha de borrado a su celda correspondiente

    0 significa que fue borrado
"""


def borrar_material(request, id_material):
    material = get_object_or_404(RelacionRecetaMaterial, pk=id_material)
    # id_receta = material.receta.id
    material.status = 0
    material.save()
    # messages.add_message(request, SUCCESS, 'Receta borrada exitosamente.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
