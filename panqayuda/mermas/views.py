from django.shortcuts import render
from paquetes.models import PaqueteInventario
from .forms import MermaPaqueteForm
import datetime

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
            else if pack.cantidad == Merma.cantidad :
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


# Create your views here.
