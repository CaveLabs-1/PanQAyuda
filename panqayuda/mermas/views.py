from django.shortcuts import render
from paquetes.models import PaqueteInventario
from materiales.models import MaterialInventario
from receta.models import RecetaInventario
from .forms import MermaPaqueteForm
import datetime

def agregar_merma_paquetes(request):
    newMermaPaqueteForm = MermaPaqueteForm()
    if request.method == 'POST':
        newMermaPaqueteForm = MermaPaqueteForm(request.POST)
        if newMermaPaqueteForm.is_valid():
            Merma = newMermaPaqueteForm.save(commit=False)
            #esto regresa el paquete del inventario que se debe borrar
            pack = PaqueteInventario.objects.filter(id=merma.nombre.id)
            if pack.cantidad < merma.cantidad :
                messages.success(request, 'No hay inventario suficiente de este paquete')
                context = {
                    'MermaPack': newMermaPaqueteForm,
                }
                return render(request, 'mermas/MagregarPack.html', context)
            else if pack.cantidad == merma.cantidad :
                merma.save()
                pack.delete()
                message.success(request, 'Se ha agregado la merma exitosamente')
                return render(reverse('mermas:lista_mermas'))
            else :
                pack.cantidad -= merma.cantidad
                merma.save()
                message.success(request, 'Se ha agregado la merma exitosamente')
                return render(reverse('mermas:lista_mermas'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo agregar la merma.')
            context = {
                'MermaPack': newMermaPaqueteForm,
            }
            return render(request, 'mermas/MagregarPack.html', context)
    else :
        return render(reverse('mermas:lista_mermas'))

def agregar_merma_materiales(request):
    newMermaMaterialForm = MermaMaterialForm()
    if request.method == 'POST':
        newMermaMaterialForm = MermaMaterialForm(request.POST)
        if newMermaMaterialForm.is_valid():
            merma = newMermaMaterialForm.save(commit=False)
            #Regresa la Material Prima del inventario que se deve de borrar
            pack = MaterialInventario.objects.filter(id=merma.nombre.id)
            if pack.cantidad < merma.cantidad :
                messages.success(request, 'No hay inventario suficiente de esta Materia Prima')
                context = {
                    'MermaPack': newMermaMaterialForm,
                }
                return render(request, 'mermas/MermaMaterial.html', context)
            elif pack.cantidad == merma.cantidad :
                merma.save()
                pack.delete()
                message.success(request, 'Se ha agregado la merma de Materia Prima exitosamente')
                return render(reverse('mermas:lista_mermas'))
            else :
                pack.cantidad -= merma.cantidad
                merma.save()
                message.success(request, 'Se ha agregado la merma de Materia Prima exitosamente')
                return render(reverse('mermas:lista_mermas'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo agregar la merma.')
            context = {
                'MermaPack': newMermaMaterialForm,
            }
            return render(request, 'mermas/MermaMaterial.html', context)
    else :
        return render(reverse('mermas:lista_mermas'))




def agregar_merma_recetas(request):
    newMermaRecetaForm = MermaRecetaForm()
    if request.method == 'POST':
        newMermaRecetaForm = MermaRecetaForm(request.POST)
        if newMermaRecetaForm.is_valid():
            merma = newMermaRecetaForm.save(commit=False)
            #Regresa la Material Prima del inventario que se deve de borrar
            pack = RecetaInventario.objects.filter(id=merma.nombre.id)
            if pack.cantidad < merma.cantidad :
                messages.success(request, 'No hay inventario suficiente de esta Materia Prima')
                context = {
                    'MermaPack': newMermaRecetaForm,
                }
                return render(request, 'mermas/MermaReceta.html', context)
            elif pack.cantidad == merma.cantidad :
                merma.save()
                pack.delete()
                message.success(request, 'Se ha agregado la merma de Producto Semi-Terminado exitosamente')
                return render(reverse('mermas:lista_mermas'))
            else :
                pack.cantidad -= merma.cantidad
                merma.save()
                message.success(request, 'Se ha agregado la merma de Producto Semi-Terminado exitosamente')
                return render(reverse('mermas:lista_mermas'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo agregar la merma.')
            context = {
                'MermaPack': newMermaRecetaForm,
            }
            return render(request, 'mermas/MermaReceta.html', context)
    else :
        return render(reverse('mermas:lista_mermas'))
# Create your views here.
