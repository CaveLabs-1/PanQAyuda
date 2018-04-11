from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from paquetes.models import PaqueteInventario
from .forms import MermaPaqueteForm
from .models import MermaReceta, MermaPaquete, MermaMaterial
from django.http import HttpResponseRedirect, HttpResponse
from panqayuda.decorators import group_required
import datetime

@group_required('admin')
def lista_mermas_receta(request):
    mermas = list(MermaReceta.objects.all())
    return render(request, 'mermas/lista_mermas_receta.html', {'mermas': mermas})

@group_required('admin')
def lista_mermas_paquete(request):
    mermas = list(MermaPaquete.objects.all())
    forma = MermaPaqueteForm()
    # return render(request, 'mermas/lista_mermas_paquete.html', {'mermas': mermas})
    return render (request, 'mermas/lista_mermas_paquete.html', {'forma': forma, 'mermas': mermas})

@group_required('admin')
def lista_mermas_material(request):
    mermas = list(MermaMaterial.objects.all())
    return render(request, 'mermas/lista_mermas_material.html', {'mermas': mermas})

def agregar_merma_paquetes(request):
    if request.method == 'POST':
        newMermaPaqueteForm = MermaPaqueteForm(request.POST)
        if newMermaPaqueteForm.is_valid():
            Merma = newMermaPaqueteForm.save(commit=False)
            #esto regresa el paquete del inventario que se debe borrar
            pack = PaqueteInventario.objects.filter(id=Merma.nombre.id)
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
                message.success(request, 'Se ha agregado la merma exitosamente')
                return render(reverse('mermas:lista_mermas_paquete'))
            else :
                pack.cantidad -= Merma.cantidad
                Merma.save()
                message.success(request, 'Se ha agregado la merma exitosamente')
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
