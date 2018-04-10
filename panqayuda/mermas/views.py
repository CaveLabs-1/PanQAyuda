from django.shortcuts import render
from paquetes.models import PaqueteInventario
from .forms import MermaPaqueteForm
from .models import MermaReceta, MermaPaquete, MermaMaterial
from panqayuda.decorators import group_required
import datetime

@group_required('admin')
def lista_mermas(request):
    mermas = list(MermaReceta.objects.all())
    mermas += list(MermaPaquete.objects.all())
    mermas += list(MermaMaterial.objects.all())
    return render(request, 'mermas/lista_mermas.html', {'mermas': mermas})

def agregar_merma_paquetes(request):
    newMermaPaqueteForm = MermaPaqueteForm()
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
                return render(request, 'mermas/MagregarPack.html', context)
            elif pack.cantidad == Merma.cantidad :
                Merma.save()
                pack.delete()
                message.success(request, 'Se ha agregado la merma exitosamente')
                return render(reverse('mermas:lista_mermas'))
            else :
                pack.cantidad -= Merma.cantidad
                Merma.save()
                message.success(request, 'Se ha agregado la merma exitosamente')
                return render(reverse('mermas:lista_mermas'))
        else :
            messages.success(request, 'Hubo un error en la forma')
            context = {
                'MermaPack': newMermaPaqueteForm,
            }
            return render(request, 'mermas/MagregarPack.html', context)
    else :
        return render(rreverse('mermas:lista_mermas'))
