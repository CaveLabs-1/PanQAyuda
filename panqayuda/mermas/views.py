from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from paquetes.models import PaqueteInventario, Paquete
from materiales.models import MaterialInventario, Material
from recetas.models import RecetaInventario, Receta
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
    recetas_catalogo = Receta.objects.filter(deleted_at__isnull=True)
    return render (request, 'mermas/lista_mermas_receta.html', {'forma': forma, 'mermas': mermas, 'recetas_catalogo':recetas_catalogo})
    # return render(request, 'mermas/lista_mermas_receta.html', {'mermas': mermas})

@group_required('admin')
def lista_mermas_paquete(request):
    mermas = list(MermaPaquete.objects.all())
    forma = MermaPaqueteForm()
    paquetes_catalogo = Paquete.objects.filter(deleted_at__isnull=True)
    print(paquetes_catalogo)
    return render (request, 'mermas/lista_mermas_paquete.html', {'forma': forma, 'mermas': mermas,'paquetes_catalogo':paquetes_catalogo})

@group_required('admin')
def lista_mermas_material(request):
    materiales_catalogo = Material.objects.filter(deleted_at__isnull=True)
    mermas = list(MermaMaterial.objects.all())
    forma = MermaMaterialForm()
    return render (request, 'mermas/lista_mermas_material.html', {'forma': forma, 'mermas': mermas, 'materiales_catalogo':materiales_catalogo})
    # return render(request, 'mermas/lista_mermas_material.html', {'mermas': mermas})


#Funcionalidad agregar merma de paquetes
@group_required('admin')
def agregar_merma_paquetes(request):
    if request.method == 'POST':
        newMermaPaqueteForm = MermaPaqueteForm(request.POST)
        if newMermaPaqueteForm.is_valid():
            Merma = newMermaPaqueteForm.save(commit=False)
            #esto regresa el paquete del inventario que se debe borrar
            pack = PaqueteInventario.objects.get(id=Merma.nombre.id)
            if pack.disponibles() < Merma.cantidad :
                messages.success(request, 'Este producto terminado solo tiene ' + str(pack.disponibles()) + " paquetes disponibles.")
                context = {
                    'MermaPack': newMermaPaqueteForm,
                }
                # return render(request, 'mermas/MagregarPack.html', context)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_paquete'))
            elif pack.disponibles() == Merma.cantidad :
                Merma.save()
                pack.ocupados  = pack.cantidad
                pack.save()
                messages.success(request, 'Se quitaron ' + str(Merma.cantidad) + ' paquetes de ' + pack.nombre.nombre)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_paquete'))
            else :
                pack.ocupados += Merma.cantidad
                Merma.save()
                pack.save()
                messages.success(request, 'Se quitaron ' + str(Merma.cantidad) + ' paquetes de ' + pack.nombre.nombre)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_paquete'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo completar la acción con éxito.')
            context = {
                'MermaPack': newMermaPaqueteForm,
            }
            # return render(request, 'mermas/MagregarPack.html', context)
            return HttpResponseRedirect(reverse('mermas:lista_mermas_paquete'))
    else :
        forma = MermaPaqueteForm()
        return render (request, 'mermas/lista_mermas_paquete.html', {'forma': forma, 'mermas': lista_mermas_paquete})
        # return render(reverse('mermas:lista_mermas_paquete'))

@group_required('admin')
def agregar_merma_materiales(request):
    if request.method == 'POST':
        newMermaMaterialForm = MermaMaterialForm(request.POST)
        if newMermaMaterialForm.is_valid():
            Merma = newMermaMaterialForm.save(commit=False)
            #Regresa la Material Prima del inventario que se debe de borrar
            pack = MaterialInventario.objects.get(id=Merma.nombre.id)
            if pack.porciones_disponible < Merma.cantidad :
                messages.success(request, 'Esta materia prima solo tiene ' + str(pack.porciones_disponible) +  " "+ + "disponibles.")
                context = {
                    'MermaPack': newMermaMaterialForm,
                }
                # return render(request, 'mermas/MermaMaterial.html', context)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_material'))
            elif pack.porciones_disponible == Merma.cantidad:
                Merma.save()
                pack.porciones_disponible = 0
                pack.save()
                messages.success(request, 'Se quitaron ' + str(Merma.cantidad) + ' unidad de ' + pack.material.nombre)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_material'))
            else :
                pack.porciones_disponible -= Merma.cantidad
                Merma.save()
                pack.save()
                messages.success(request, 'Se quitaron ' + str(Merma.cantidad) + ' unidad de ' + pack.material.nombre)
                # return render(reverse('mermas:lista_mermas_material'))
                return HttpResponseRedirect(reverse('mermas:lista_mermas_material'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo completar la acción con éxito.')
            context = {
                'MermaPack': newMermaMaterialForm,
            }
            # return render(request, 'mermas/MermaMaterial.html', context)
            return HttpResponseRedirect(reverse('mermas:lista_mermas_material'))
    else :
        forma = MermaMaterialForm()
        return render (request, 'mermas/lista_mermas_material.html', {'forma': forma, 'mermas': lista_mermas_material})
        # return render(reverse('mermas:lista_mermas_material'))

@group_required('admin')
def agregar_merma_recetas(request):
    if request.method == 'POST':
        newMermaRecetaForm = MermaRecetaForm(request.POST)
        if newMermaRecetaForm.is_valid():
            merma = newMermaRecetaForm.save(commit=False)
            #Regresa la Material Prima del inventario que se deve de borrar
            pack = RecetaInventario.objects.get(id=merma.nombre.id)
            if pack.disponibles() < merma.cantidad :
                messages.success(request, 'Este producto semiterminado solo tiene ' + str(pack.disponibles()) + " porciones disponibles")
                context = {
                    'MermaPack': newMermaRecetaForm,
                }
                return HttpResponseRedirect(reverse('mermas:lista_mermas_receta'))
                # return render(request, 'mermas/MermaReceta.html', context)
            elif pack.disponibles() == merma.cantidad :
                merma.save()
                pack.ocupados = pack.cantidad
                pack.save()
                messages.success(request, 'Se quitaron ' + str(merma.cantidad) + ' porciones de ' + pack.nombre.nombre)
                return HttpResponseRedirect(reverse('mermas:lista_mermas_receta'))
            else :
                pack.ocupados += merma.cantidad
                merma.save()
                pack.save()
                messages.success(request, 'Se quitaron ' + str(merma.cantidad) + ' porciones de ' + pack.nombre.nombre)
                # return render(reverse('mermas:lista_mermas_receta'))
                return HttpResponseRedirect(reverse('mermas:lista_mermas_receta'))
        else :
            messages.success(request, 'Hubo un error en la forma y no se pudo completar la acción con éxito.')
            context = {
                'MermaPack': newMermaRecetaForm,
            }
            return HttpResponseRedirect(reverse('mermas:lista_mermas_receta'))
            # return render(request, 'mermas/MermaReceta.html', context)
    else :
        forma = MermaRecetaForm()
        return render(request, 'mermas/lista_mermas_receta.html', {'forma': forma, 'mermas': lista_mermas_receta})
        # return render(reverse('mermas:lista_mermas_receta'))

#Devuelve una respuesta con una lista de opciones para un select con los paquetes inventario del paquete solicitado
@group_required('admin')
def obtener_paquetes_ajuste_inventario(request):
    id_paquete_catalogo = int(request.GET.get('id_paquete_catalogo'))
    paquete_catalogo = Paquete.objects.get(pk=id_paquete_catalogo)
    #Obtener los paquetes en inventario
    paquetes_inventario =  paquete_catalogo.obtener_paquetes_inventario_con_caducados()
    #Renderizar las opciones y enviarlas
    response=render_to_string('mermas/opciones_paquete_inventario.html', {'paquetes_inventario':paquetes_inventario},request=request)
    return HttpResponse(response)

#Devuelve una respuesta con una lista de opciones para un select con las recetas inventario de la receta solicitada
@group_required('admin')
def obtener_recetas_ajuste_inventario(request):
    receta_catalogo_id = int(request.GET.get('receta_catalogo_id'))
    receta_catalogo = Receta.objects.get(pk=receta_catalogo_id)
    #Obtener los paquetes en inventario
    recetas_inventario =  receta_catalogo.obtener_recetas_inventario_con_caducados()
    #Renderizar las opciones y enviarlas
    response=render_to_string('mermas/opciones_receta_inventario.html', {'recetas_inventario':recetas_inventario},request=request)
    return HttpResponse(response)

#Devuelve una lista de opciones para un select con los materiales del inventario para ciero material solicitado
@group_required('admin')
def obtener_materiales_ajuste_inventario(request):
    #Obtener el material del catálogo
    material_catalogo_id = request.GET.get('material_catalogo_id')
    material_catalogo = Material.objects.get(pk=material_catalogo_id)

    #Obtener materiales del inventario
    materiales_inventario = material_catalogo.obtener_materiales_inventario_con_caducados()

    #Renderizar opciones
    response = render_to_string('mermas/opciones_material_inventario.html', {'materiales_inventario':materiales_inventario}, request=request)

    return HttpResponse(response)
