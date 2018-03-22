from django.shortcuts import render, get_object_or_404, redirect
from paquetes.models import Paquete, PaqueteInventario
from paquetes.models import RecetasPorPaquete
from recetas.models import Receta, RecetaInventario
from paquetes.forms import FormPaquete, FormRecetasPorPaquete, FormPaqueteInventario, FormEditarPaquete
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.db.models.functions import Concat
from panqayuda.decorators import group_required
import datetime
import json

#indice
@group_required('admin')
def lista_paquetes(request):
    lista_de_paquetes=Paquete.objects.filter(estatus=1).filter(deleted_at__isnull=True)
    return render(request, 'paquetes/ver_paquetes.html', {'paquetes':lista_de_paquetes})

#agregar paquete
@group_required('admin')
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

@group_required('admin')
def borrar_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, pk=id_paquete)
    paquete.estatus = 0
    paquete.deleted_at = datetime.datetime.now()
    paquete.save()
    messages.success(request, '¡Se ha borrado el paquete del catálogo!')
    return redirect('paquetes:lista_paquetes')

@group_required('admin')
def lista_paquete_inventario(request):
    paquetes=PaqueteInventario.objects.filter(deleted_at__isnull=True).filter(estatus=1)
    catalogo_paquetes=Paquete.objects.filter(deleted_at__isnull=True).filter(estatus=1)

    for catalogo_paquete in catalogo_paquetes:
         aux= PaqueteInventario.objects.filter(nombre_id=catalogo_paquete.id).filter(deleted_at__isnull=True).aggregate(Sum('cantidad'))
         catalogo_paquete.total=aux['cantidad__sum']

    return render(request, 'paquetes/lista_paquetes_inventario.html', {'paquetes':paquetes, 'catalogo_paquetes':catalogo_paquetes})

@group_required('admin')
def paquetes_por_catalogo(request):
    if request.method == 'POST':
        id_paquete = request.POST.get('id_paquete')
        paquete = Paquete.objects.get(pk=id_paquete)
        detalle_paquetes_en_inventario = PaqueteInventario.objects.filter(nombre_id=id_paquete, deleted_at__isnull=True)
        response = render_to_string('paquetes/lista_detalle_paquetes_inventario.html', {'detalle_paquetes_en_inventario': detalle_paquetes_en_inventario, 'paquete': paquete})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

@group_required('admin')
def agregar_paquete_inventario(request):
    if request.method == 'POST':
        forma_post=FormPaqueteInventario(request.POST or None)
        if forma_post.is_valid():
            #Obtener paquete
            id_paquete = request.POST.get('nombre')
            paquete = Paquete.objects.get(pk=id_paquete)

            #Obtener recetas del paquete
            recetas = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)

            # Verificar que exista cantidad suficiente para crear el paquete de cada receta
            for receta in recetas:
                #Número de paquetes a crear
                cantidad_post = forma_post.instance.cantidad
                #Total de piezas necesitadas para esta receta
                cantidad_real = cantidad_post * receta.cantidad
                #Cantidad disponible en inventario
                cantidad_inv = RecetaInventario.obtener_cantidad_inventario(receta.receta)

                if cantidad_real > cantidad_inv:
                    print(cantidad_real)
                    print(cantidad_inv)
                    messages.error(request, 'No hay inventario suficiente para agregar este paquete')
                    return HttpResponseRedirect(reverse('paquetes:agregar_inventario'))

            # #Restar inventario
            for receta in recetas:
                cantidad_post = forma_post.instance.cantidad
                #Obtener recetas del inventario disponibles para restar ordenadas por fecha de caducidad
                recetas_inventario = RecetaInventario.obtener_disponibles(receta.receta)
                cantidad_necesitada = cantidad_post * receta.cantidad
                for receta_inventario in recetas_inventario:
                #La necesitada es mayor que la cantidad que este 'lote' tiene
                    if cantidad_necesitada > receta_inventario.disponible:
                        cantidad_necesitada-=receta_inventario.disponible
                        receta_inventario.ocupados = receta_inventario.cantidad
                        receta_inventario.save()
                    #Este 'lote' satisface la cantidad necesitada para el paquete
                    else:
                        receta_inventario.ocupados+=cantidad_necesitada
                        receta_inventario.save()
                        break
            forma_post.save()
            messages.success(request, 'Se ha agregado el paquete al inventario')
            return HttpResponseRedirect(reverse('paquetes:lista_paquete_inventario'))
        else:
            messages.error(request, 'Hubo un error y no se agregó el paquete al inventario.')
            return HttpResponseRedirect(reverse('paquetes:agregar_paquete_inventario'))
    else:
        #print("no es post")
        forma=FormPaqueteInventario()
        messages.error(request, 'Hubo un error con la peticion')
        paquetes = Paquete.objects.filter(deleted_at__isnull=True).order_by("nombre")
        return render(request, 'paquetes/agregar_inventario.html', {'paquetes': paquetes, 'forma':forma})

@group_required('admin')
def borrar_paquete_inventario(request, id_paquete_inventario):
    paquete_inventario = get_object_or_404(PaqueteInventario, pk=id_paquete_inventario)
    paquete_inventario.estatus = 0
    paquete_inventario.deleted_at = datetime.datetime.now()
    paquete_inventario.save()
    messages.success(request, 'Se ha borrado el paquete del inventario')
    return redirect('paquetes:lista_paquete_inventario')


#US22
@group_required('admin')
def editar_paquete_inventario(request, id_paquete):
    paquete_inventario = get_object_or_404(PaqueteInventario, pk=id_paquete)
    print('no llega ni a post')
    if request.method == "POST":
        print('ya llego a post')
        form = FormEditarPaquete(request.POST or None, instance=paquete_inventario)
        if form.is_valid():
            print('la forma es valida')
            paquete_inventario = form.save()
            paquete_inventario.save()
            messages.success(request, '¡Se ha editado la paquete_inventario exitosamente!')
            return redirect('paquetes:lista_paquete_inventario')
        print(form.errors)
    else:
        form = FormEditarPaquete()
    return render(request, 'paquetes/editar_paquete_inventario.html', {'form': form, 'paquete_inventario': paquete_inventario})



#agregar recetas a paquete
@group_required('admin')
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

@group_required('admin')
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

@group_required('admin')
def paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, id=id_paquete)
    recetas = recetas = Receta.objects.filter(deleted_at = null, paquete = paquete)
    return render(request, 'paquetes/paquete.html', {'paquete': paquete, 'recetas': recetas})

#editar paquete
@group_required('admin')
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
