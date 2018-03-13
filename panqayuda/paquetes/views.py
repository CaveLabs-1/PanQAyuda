from django.shortcuts import render, get_object_or_404, redirect
from paquetes.models import Paquete, PaqueteInventario
from paquetes.models import RecetasPorPaquete
from recetas.models import Receta
from paquetes.forms import FormPaquete, FormRecetasPorPaquete, FormPaqueteInventario
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.db.models.functions import Concat
import datetime
import json

#indice
def lista_paquetes(request):
    lista_de_paquetes=Paquete.objects.filter(estatus=1).filter(deleted_at__isnull=True)
    return render(request, 'paquetes/ver_paquetes.html', {'paquetes':lista_de_paquetes})

#agregar paquete
def agregar_paquete(request):
    if request.method == 'POST':
        forma=FormPaquete(request.POST)
        if forma.is_valid():
            forma.save()
            messages.success(request, '¡Se ha agregado el paquete al catálogo!')
            paquete = Paquete.objects.latest('id')
            return HttpResponseRedirect(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        else:
            messages.info(request, 'Hubo un error y no se agregó el paquete. Inténtalo de nuevo.')
    else:
        forma=FormPaquete()
    return render(request, 'paquetes/agregar_paquete.html', {'forma':forma})


def borrar_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, pk=id_paquete)
    paquete.estatus = 0
    paquete.deleted_at = datetime.datetime.now()
    paquete.save()
    messages.success(request, '¡Se ha borrado el paquete del catálogo!')
    return redirect('paquetes:lista_paquete_inventario')


def lista_paquete_inventario(request):
    paquetes=PaqueteInventario.objects.filter(deleted_at__isnull=True).filter(estatus=1)
    catalogo_paquetes=Paquete.objects.filter(deleted_at__isnull=True).filter(estatus=1)

    for catalogo_paquete in catalogo_paquetes:
         aux= PaqueteInventario.objects.filter(nombre_id=catalogo_paquete.id).filter(deleted_at__isnull=True).aggregate(Sum('cantidad'))
         catalogo_paquete.total=aux['cantidad__sum']

    return render(request, 'paquetes/lista_paquetes_inventario.html', {'paquetes':paquetes, 'catalogo_paquetes':catalogo_paquetes})

def paquetes_por_catalogo(request):
    if request.method == 'POST':
        id_paquete = request.POST.get('id_paquete')
        paquete = Paquete.objects.get(pk=id_paquete)
        detalle_paquetes_en_inventario = PaqueteInventario.objects.filter(nombre_id=id_paquete, deleted_at__isnull=True)
        response = render_to_string('paquetes/lista_detalle_paquetes_inventario.html', {'detalle_paquetes_en_inventario': detalle_paquetes_en_inventario, 'paquete': paquete})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

def agregar_paquete_inventario(request):
    if request.method == 'POST':
        #print("si es post")
        forma_post=FormPaqueteInventario(request.POST or None)
        #print(forma_post)
        if forma_post.is_valid():
            #print("entró al if de la forma validada")
            id_paquete = request.POST.get('nombre')
            paquete = Paquete.objects.get(pk=id_paquete)
            # recetas = RecetasPorPaquete.recetas_paquete(paquete)
            recetas = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)
            #print (recetas)

            # Cuando exista inventario de materia prima esto va a servir
            # for receta in recetas:
            #     print("entró en primer for")
            #     cantidad_post = forma_post.instance.cantidad
            #     cantidad_inv = receta.receta.cantidad
            #     cantidad_real = cantidad_post * receta.cantidad
            #     if cantidad_real > cantidad_inv:
            #         messages.error(request, 'No hay inventario suficiente para agregar este paquete')
            #         return HttpResponseRedirect(reverse('paquetes:agregar_inventario'))
            # #Restar inventario
            #
            # for receta in recetas:
            #     print("entró en segundo for")
            #     cantidad_a_cambiar = cantidad_inv - cantidad_real
            #     cantidad_inv = cantidad_a_cambiar
            #     receta.receta.cantidad = cantidad_a_cambiar
            #     receta.receta.save()
            forma_post.save()
            messages.success(request, 'Se ha agregado el paquete al inventario')
            paquete = PaqueteInventario.objects.latest('id')
            return HttpResponseRedirect(reverse('paquetes:lista_paquete_inventario'))
        else:
            #print("la forma no es valida")
            messages.error(request, 'Hubo un error y no se agregó el paquete al inventario.')
            return HttpResponseRedirect(reverse('paquetes:agregar_inventario'))
    else:
        #print("no es post")
        forma=FormPaqueteInventario()
        messages.error(request, 'Hubo un error con la peticion')
        paquetes = Paquete.objects.filter(deleted_at__isnull=True).order_by("nombre")
        return render(request, 'paquetes/agregar_inventario.html', {'paquetes': paquetes, 'forma':forma})

def borrar_paquete_inventario(request, id_paquete_inventario):
    paquete_inventario = get_object_or_404(PaqueteInventario, pk=id_paquete_inventario)
    paquete_inventario.estatus = 0
    paquete_inventario.deleted_at = datetime.datetime.now()
    paquete_inventario.save()
    messages.success(request, 'Se ha borrado el paquete del inventario')
    return redirect('paquetes:lista_paquete_inventario')


def editar_paquete_inventario(request, id_paquete_inventario):
    paquete_inventario = get_object_or_404(PaqueteInventario, pk=id_paquete_inventario)
    if request.method == "POST":
        form = FormPaqueteInventario(request.POST or None, instance=paquete_inventario)
        if form.is_valid():
            paquete_inventario = form.save()
            paquete_inventario.save
            messages.success(request, 'Se ha editado el paquete del inventario exitosamente!')
            return render(request, 'paquete_inventarios/paquete_inventario.html', {'paquete_inventario': paquete_inventario})
    else:
        form = PaqueteInventario()
    return render(request, 'paquete_inventarios/editar_paquete_inventario.html', {'form': form, 'paquete_inventario': paquete_inventario})



#agregar recetas a paquete
def agregar_recetas_a_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, id=id_paquete)
    #Checar que sea un paquete activo
    if paquete.estatus == 0 or paquete.deleted_at != None:
        raise Http404
    forma = FormRecetasPorPaquete()
    recetas_por_paquete = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)
    recetas = Receta.objects.filter(deleted_at__isnull=True).exclude(id__in=recetas_por_paquete.values('receta'))
    formahtml = render_to_string('paquetes/forma_agregar_recetas_paquete.html', {'forma': forma, 'recetas': recetas, 'paquete': paquete})
    lista_recetas = render_to_string('paquetes/lista_recetas_por_paquete.html', {'recetas_por_paquete': recetas_por_paquete})
    return render(request, 'paquetes/agregar_recetas_a_paquete.html', {'formahtml': formahtml, 'lista_recetas':lista_recetas, 'recetas': recetas, 'paquete': paquete, 'forma': forma})

def agregar_receta_a_paquete(request):
    if request.method == 'POST':
        forma = FormRecetasPorPaquete(request.POST)
        #Crear relación si la forma es válida, regresar error si no.
        if forma.is_valid():
            id_receta = int(request.POST.get('receta'))
            receta = get_object_or_404(Receta, id=id_receta)
            cantidad = int(request.POST.get('cantidad'))
            id_paquete = int(request.POST.get('paquete'))
            paquete = get_object_or_404(Paquete, id=id_paquete)
            forma = FormRecetasPorPaquete()
            RecetasPorPaquete.objects.create(paquete = paquete,receta = receta, cantidad= cantidad )
            recetas_por_paquete = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)
            recetas = Receta.objects.filter(deleted_at__isnull=True).exclude(id__in=recetas_por_paquete.values('receta'))
            formahtml = render_to_string('paquetes/forma_agregar_recetas_paquete.html',
                                         {'forma': forma, 'recetas': recetas, 'paquete': paquete})
            lista_recetas = render_to_string('paquetes/lista_recetas_por_paquete.html',
                                             {'recetas_por_paquete': recetas_por_paquete})
            data = '' + formahtml + lista_recetas + ''
            return HttpResponse(data)
        else:
            mensaje_error = ""
            for field,errors in forma.errors.items():
                 for error in errors:
                     mensaje_error+=error + "\n"
            return HttpResponseNotFound('Hubo un problema agregando la receta al paquete: '+ mensaje_error)


def paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, id=id_paquete)
    recetas = recetas = Receta.objects.filter(deleted_at = null, paquete = paquete)
    return render(request, 'paquetes/paquete.html', {'paquete': paquete, 'recetas': recetas})

#editar paquete
def editar_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, pk=id_paquete)
    if request.method == "POST":
        forma = FormPaquete(request.POST or None, instance=paquete)
        if forma.is_valid():
            paquete = forma.save()
            return HttpResponseRedirect(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        else:
            messages.info(request, 'Hubo un error con la peticion')
            return HttpResponseRedirect(reverse('paquetes:editar_paquete', kwargs={'id_paquete':paquete.id}))
    else:
        forma = FormPaquete(initial={"nombre":paquete.nombre, "precio":paquete.precio})
        return render(request, 'paquetes/editar_paquete.html', {'forma':forma, 'paquete':paquete})
