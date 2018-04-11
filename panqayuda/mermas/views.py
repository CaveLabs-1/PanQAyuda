from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from paquetes.models import PaqueteInventario
from materiales.models import MaterialInventario
from recetas.models import RecetaInventario
from .forms import MermaPaqueteForm
from .forms import MermaMaterialForm
from .forms import MermaRecetaForm
from .models import MermaReceta, MermaPaquete, MermaMaterial
from django.http import HttpResponseRedirect, HttpResponse
from panqayuda.decorators import group_required
import datetime

@group_required('admin')
def lista_mermas_receta(request):
    mermas = list(MermaReceta.objects.all())
    forma = MermaRecetaForm()
    return render (request, 'mermas/lista_mermas_receta.html', {'forma': forma, 'mermas': mermas})
    # return render(request, 'mermas/lista_mermas_receta.html', {'mermas': mermas})

@group_required('admin')
def lista_mermas_paquete(request):
    mermas = list(MermaPaquete.objects.all())
    forma = MermaPaqueteForm()
    # return render(request, 'mermas/lista_mermas_paquete.html', {'mermas': mermas})
    return render (request, 'mermas/lista_mermas_paquete.html', {'forma': forma, 'mermas': mermas})

@group_required('admin')
def lista_mermas_material(request):
    mermas = list(MermaMaterial.objects.all())
    forma = MermaMaterialForm()
    return render (request, 'mermas/lista_mermas_material.html', {'forma': forma, 'mermas': mermas})
    # return render(request, 'mermas/lista_mermas_material.html', {'mermas': mermas})

def agregar_merma_paquetes(request):
    if request.method == 'POST':
        newMermaPaqueteForm = MermaPaqueteForm(request.POST)
        if newMermaPaqueteForm.is_valid():
            Merma = newMermaPaqueteForm.save(commit=False)
            #esto regresa el paquete del inventario que se debe borrar
            pack = PaqueteInventario.objects.get(id=Merma.nombre.id)
            if pack.cantidad < Merma.cantidad :
                messages.success(request, 'No hay inventario suficiente de este paquete')
                context = {
                    'MermaPack': newMermaPaqueteForm,
                }
                # return render(request, 'mermas/MagregarPack.html', context)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_paquete'))
            elif pack.cantidad == Merma.cantidad :
                Merma.save()
                pack.delete()
                messages.success(request, 'Se ha agregado la merma exitosamente')
                return render(reverse('mermas:lista_mermas_paquete'))
            else :
                pack.cantidad -= Merma.cantidad
                Merma.save()
                messages.success(request, 'Se ha agregado la merma exitosamente')
                return render(reverse('mermas:lista_mermas_paquete'))
        else :
            messages.success(request, 'Hubo un error en la forma')
            context = {
                'MermaPack': newMermaPaqueteForm,
            }
            # return render(request, 'mermas/MagregarPack.html', context)
            return HttpResponseRedirect(reverse('mermas:lista_mermas_paquete'))
    else :
        forma = MermaPaqueteForm()
        return render (request, 'mermas/lista_mermas_paquete.html', {'forma': forma, 'mermas': lista_mermas_paquete})
        # return render(reverse('mermas:lista_mermas_paquete'))

def agregar_merma_materiales(request):
    if request.method == 'POST':
        newMermaMaterialForm = MermaMaterialForm(request.POST)
        if newMermaMaterialForm.is_valid():
            Merma = newMermaMaterialForm.save(commit=False)
            #Regresa la Material Prima del inventario que se deve de borrar
            pack = MaterialInventario.objects.get(id=Merma.nombre.id)
            if pack.cantidad < Merma.cantidad :
                messages.success(request, 'No hay inventario suficiente de esta Materia Prima')
                context = {
                    'MermaPack': newMermaMaterialForm,
                }
                # return render(request, 'mermas/MermaMaterial.html', context)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_material'))
            elif pack.cantidad == Merma.cantidad :
                Merma.save()
                pack.delete()
                messages.success(request, 'Se ha agregado la merma de Materia Prima exitosamente')
                return render(reverse('mermas:lista_mermas_material'))
            else :
                pack.cantidad -= Merma.cantidad
                Merma.save()
                messages.success(request, 'Se ha agregado la merma de Materia Prima exitosamente')
                # return render(reverse('mermas:lista_mermas_material'))
                return HttpResponseRedirect(reverse('mermas:lista_mermas_material'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo agregar la merma.')
            context = {
                'MermaPack': newMermaMaterialForm,
            }
            # return render(request, 'mermas/MermaMaterial.html', context)
            return HttpResponseRedirect(reverse('mermas:lista_mermas_material'))
    else :
        forma = MermaMaterialForm()
        return render (request, 'mermas/lista_mermas_material.html', {'forma': forma, 'mermas': lista_mermas_material})
        # return render(reverse('mermas:lista_mermas_material'))


def agregar_merma_recetas(request):
    if request.method == 'POST':
        newMermaRecetaForm = MermaRecetaForm(request.POST)
        if newMermaRecetaForm.is_valid():
            merma = newMermaRecetaForm.save(commit=False)
            #Regresa la Material Prima del inventario que se deve de borrar
            pack = RecetaInventario.objects.get(id=merma.nombre.id)
            if pack.cantidad < merma.cantidad :
                messages.success(request, 'No hay inventario suficiente de esta Materia Prima')
                context = {
                    'MermaPack': newMermaRecetaForm,
                }
                return HttpResponseRedirect(reverse('mermas:lista_mermas_receta'))
                # return render(request, 'mermas/MermaReceta.html', context)
            elif pack.cantidad == merma.cantidad :
                merma.save()
                pack.delete()
                messages.success(request, 'Se ha agregado la merma de Producto Semi-Terminado exitosamente')
                return render(reverse('mermas:lista_mermas_receta'))
            else :
                pack.cantidad -= merma.cantidad
                merma.save()
                messages.success(request, 'Se ha agregado la merma de Producto Semi-Terminado exitosamente')
                # return render(reverse('mermas:lista_mermas_receta'))
                return HttpResponseRedirect(reverse('mermas:lista_mermas_receta'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo agregar la merma.')
            context = {
                'MermaPack': newMermaRecetaForm,
            }
            return HttpResponseRedirect(reverse('mermas:lista_mermas_receta'))
            # return render(request, 'mermas/MermaReceta.html', context)
    else :
        forma = MermaRecetaForm()
        return render (request, 'mermas/lista_mermas_receta.html', {'forma': forma, 'mermas': lista_mermas_receta})
        # return render(reverse('mermas:lista_mermas_receta'))
