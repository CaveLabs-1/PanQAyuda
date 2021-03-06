from django.shortcuts import render, get_object_or_404, redirect
from paquetes.models import Paquete, PaqueteInventario
from paquetes.models import RecetasPorPaquete
from recetas.models import Receta, RecetaInventario
from paquetes.forms import FormPaquete, FormRecetasPorPaquete, FormPaqueteInventario, FormEditarPaquete
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.db.models import Sum, F
from django.db.models.functions import Concat
from panqayuda.decorators import group_required
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import json

"""
    Regresa la lista de paquetes
"""
@group_required('admin')
def lista_paquetes(request):
    lista_de_paquetes=Paquete.objects.filter(estatus=1).filter(deleted_at__isnull=True)
    return render(request, 'paquetes/ver_paquetes.html', {'paquetes':lista_de_paquetes})


"""
    En caso de GET regresa la forma para hacer el POST correspondiente
"""
@group_required('admin')
def agregar_paquete(request):
    #Revisar si se manda por POST
    if request.method == 'POST':
        #Mandar la forma
        forma=FormPaquete(request.POST)
        #Cehcar si la forma es válida
        if forma.is_valid():
            #Guardas la forma y mandas mensaje de éxito y redirige a agregar recetas a paquete
            forma.save()
            messages.success(request, '¡Se ha agregado el producto al catálogo!')
            paquete = Paquete.objects.latest('id')
            return HttpResponseRedirect(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
            #Manda mensaje de error si la forma no es válida
        else:
            messages.info(request, 'Hubo un error y no se agregó el producto terminado. Inténtalo de nuevo.')
    #Manda mensaje de error si no se manda por POST
    else:
        forma=FormPaquete()
    return render(request, 'paquetes/agregar_paquete.html', {'forma':forma})

"""
    Recibe el id de el paquete a borrar, cambia su estado a 0 y su deleted_at a
    la hora correspondiente
"""
@group_required('admin')
def borrar_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, pk=id_paquete)
    paquete.estatus = 0
    paquete.deleted_at = datetime.datetime.now()
    paquete.save()
    messages.success(request, '¡Se ha borrado el paquete del catálogo!')
    return redirect('paquetes:lista_paquetes')

"""
    Enlista los paquetes inventario que tinenen de estatus 0
"""
@group_required('admin')
def lista_paquete_inventario(request):
    paquetes=PaqueteInventario.objects.filter(deleted_at__isnull=True).filter(estatus=1)
    catalogo_paquetes=Paquete.objects.filter(deleted_at__isnull=True).filter(estatus=1)

    for catalogo_paquete in catalogo_paquetes:
         aux= PaqueteInventario.objects.filter(nombre_id=catalogo_paquete.id).filter(deleted_at__isnull=True).annotate(cantidad_disponible=F('cantidad')-F('ocupados')).aggregate(Sum('cantidad_disponible'))
         catalogo_paquete.total=aux['cantidad_disponible__sum']

    return render(request, 'paquetes/lista_paquetes_inventario.html', {'paquetes':paquetes, 'catalogo_paquetes':catalogo_paquetes})

"""
    Regresa los los paquetes inventario correspondiente
"""
@group_required('admin')
def paquetes_por_catalogo(request):
    if request.method == 'POST':
        id_paquete = request.POST.get('id_paquete')
        paquete = Paquete.objects.get(pk=id_paquete)
        detalle_paquetes_en_inventario = PaqueteInventario.objects.filter(nombre_id=id_paquete, deleted_at__isnull=True)
        response = render_to_string('paquetes/lista_detalle_paquetes_inventario.html', {'detalle_paquetes_en_inventario': detalle_paquetes_en_inventario, 'paquete': paquete})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

"""

"""
@group_required('admin')
def agregar_paquete_inventario(request):
    #Revisa que sea método post
    if request.method == 'POST':
        #Obtiene la forma
        forma_post=FormPaqueteInventario(request.POST or None)
        #Revisa que la forma sea válida
        if forma_post.is_valid():
            #Obtener paquete
            id_paquete = request.POST.get('nombre')
            paquete = Paquete.objects.get(pk=id_paquete)
            data = forma_post.cleaned_data

            cantidad_post = forma_post.instance.cantidad
            #Verificar que hay suficiente cantidad en inventario para agregar el paquete
            agregar_paquete_inventario = agregar_paquetes_inventario_recetas(paquete,cantidad_post)
            if agregar_paquete_inventario != None:
                receta = agregar_paquete_inventario.receta.nombre
                messages.success(request, 'No hay inventario suficiente de ' + receta +' para agregar este producto terminado')
                return HttpResponseRedirect(reverse('paquetes:agregar_inventario'))
            costo= costo_paquetes_inventario_recetas(paquete, cantidad_post)
            PaqueteInventario.objects.create(nombre=data['nombre'], cantidad=data['cantidad'], fecha_cad=data['fecha_cad'], costo=costo)
            messages.success(request, 'Se ha agregado el paquete al inventario')
            return HttpResponseRedirect(reverse('paquetes:lista_paquete_inventario'))
        #Si la forma no es válida, manda un mensaje de error y regresa a agregar paquete en inventario
        else:
            messages.success(request, 'Hubo un error y no se agregó el producto terminado al inventario.')
            return HttpResponseRedirect(reverse('paquetes:agregar_inventario'))
    #Si no se manda por método POST
    else:
        forma=FormPaqueteInventario()
        paquetes = Paquete.objects.filter(deleted_at__isnull=True).order_by("nombre")
        return render(request, 'paquetes/agregar_inventario.html', {'paquetes': paquetes, 'forma':forma})

@group_required('admin')
def borrar_paquete_inventario(request, id_paquete_inventario):
    paquete_inventario = get_object_or_404(PaqueteInventario, pk=id_paquete_inventario)
    cantidad = paquete_inventario.cantidad
    eliminar_paquetes_inventario_recetas(paquete_inventario.nombre, cantidad)
    paquete_inventario.estatus = 0
    paquete_inventario.deleted_at = datetime.datetime.now()
    paquete_inventario.save()
    messages.success(request, 'Se ha borrado el producto terminado del inventario')
    return redirect('paquetes:lista_paquete_inventario')

@group_required('admin')
#US22
def editar_paquete_inventario(request, id_paquete):
    paquete_inventario = get_object_or_404(PaqueteInventario, pk=id_paquete)
    if request.method == "POST":
        cantidad_anterior=paquete_inventario.cantidad
        form = FormEditarPaquete(request.POST or None, instance=paquete_inventario)
        if form.is_valid():
            cantidad_nueva = form.instance.cantidad
            if cantidad_nueva < cantidad_anterior:
                #Agregar piezas disponibles a las recetas en inventario
                cantidad = cantidad_anterior - cantidad_nueva
                eliminar_paquetes_inventario_recetas(paquete_inventario.nombre, cantidad)
            else:
                cantidad = cantidad_nueva - cantidad_anterior
                #Verificiar que hay cantidad suficiente en inventario para agregar los paquetes
                agregar_paquetes_inventario =  agregar_paquetes_inventario_recetas(paquete_inventario.nombre,cantidad)
                if agregar_paquetes_inventario != None:
                    receta = agregar_paquetes_inventario.receta.nombre
                    messages.error(request, 'No hay inventario suficiente de '+ receta +' para agregar este paquete')
                    return HttpResponseRedirect(reverse('paquetes:agregar_inventario'))

            paquete_inventario = form.save()
            paquete_inventario.save()
            messages.success(request, '¡Se ha editado el inventario de '+ paquete_inventario.nombre.nombre + ' exitosamente!')
            return redirect('paquetes:lista_paquete_inventario')
    else:
        form = FormEditarPaquete(instance=paquete_inventario)
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
    return render(request, 'paquetes/agregar_recetas_a_paquete.html',
    {'formahtml': formahtml, 'lista_recetas':lista_recetas, 'recetas': recetas, 'paquete': paquete, 'forma': forma})

@group_required('admin')
def agregar_receta_a_paquete(request):
    if request.method == 'POST':
        forma = FormRecetasPorPaquete(request.POST)
        #Crear relación si la forma es válida, regresar error si no.
        if forma.is_valid():
            id_receta = int(request.POST.get('receta'))
            receta = get_object_or_404(Receta, id=id_receta)
            cantidad = float(request.POST.get('cantidad'))
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
            return HttpResponseNotFound('Hubo un problema agregando el producto semit-terminado al producto terminado: '+ mensaje_error)

@group_required('admin')
def quitar_receta_paquete(request):
    #Obtener la relación y 'eliminarla'
    id_relacion = request.GET.get('id_relacion')
    relacion =  get_object_or_404(RecetasPorPaquete,pk=id_relacion)
    paquete = relacion.paquete
    relacion.deleted_at = timezone.now()
    relacion.save()

    #Renderizar la lista de recetas y la forma
    recetas_por_paquete = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)
    recetas = Receta.objects.filter(deleted_at__isnull=True).exclude(id__in=recetas_por_paquete.values('receta'))
    forma = FormRecetasPorPaquete()
    forma_html = render_to_string('paquetes/forma_agregar_recetas_paquete.html',{'forma': forma, 'recetas': recetas, 'paquete': paquete})
    lista_recetas = render_to_string('paquetes/lista_recetas_por_paquete.html',{'recetas_por_paquete': recetas_por_paquete})
    data = '' + forma_html + lista_recetas + ''

    #Enviar respuesta
    return HttpResponse(data)

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
            messages.info(request, 'Hubo un error en la forma. Aségurate que seleccionaste un nombre y un precio.')
            return HttpResponseRedirect(reverse('paquetes:editar_paquete', kwargs={'id_paquete':paquete.id}))
    else:
        forma = FormPaquete(initial={"nombre":paquete.nombre, "precio":paquete.precio})
        return render(request, 'paquetes/editar_paquete.html', {'forma':forma, 'paquete':paquete})

def agregar_paquetes_inventario_recetas(paquete,cantidad):
    # Obtener recetas del paquete
    recetas = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)
    # Verificar que exista cantidad suficiente para crear el paquete de cada receta
    for receta in recetas:
        # Total de piezas necesitadas para esta receta
        cantidad_real = cantidad * receta.cantidad
        # Cantidad disponible en inventario
        cantidad_inv = receta.receta.obtener_cantidad_inventario()
        # RecetaInventario.obtener_cantidad_inventario(receta.receta)

        if cantidad_real > cantidad_inv:
            return receta
    # #Restar inventario
    for receta in recetas:
        # Obtener recetas del inventario disponibles para restar ordenadas por fecha de caducidad
        recetas_inventario = RecetaInventario.obtener_disponibles(receta.receta)
        #Verificar que sea un material de empaquetado
        cantidad_necesitada = cantidad * receta.cantidad
        if receta.receta.material_empaque != None:
            #Como esta receta es un material de empaquetado, se le resta al material en lugar de a la receta
            receta.receta.material_empaque.restar_inventario(cantidad_necesitada)
        for receta_inventario in recetas_inventario:
            # La necesitada es mayor que la cantidad que este 'lote' tiene
            if cantidad_necesitada > receta_inventario.disponible:
                cantidad_necesitada -= receta_inventario.disponible
                receta_inventario.ocupados = receta_inventario.cantidad
                receta_inventario.save()
            # Este 'lote' satisface la cantidad necesitada para el paquete
            else:
                receta_inventario.ocupados += cantidad_necesitada
                receta_inventario.save()
                break

def costo_paquetes_inventario_recetas(paquete,cantidad):
    # Obtener recetas del paquete
    recetas = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)
    costo=0
    for receta in recetas:
        #Obtener recetas del inventario disponibles para restar ordenadas por fecha de caducidad
        recetas_inventario = RecetaInventario.obtener_disponibles(receta.receta)
        cantidad_necesitada = cantidad * receta.cantidad
        x = 0
        for receta_inventario in recetas_inventario:
            x += 1
            if x >= cantidad_necesitada:
                break
            costo+=receta_inventario.costo
    return costo

def eliminar_paquetes_inventario_recetas(paquete,cantidad):
    recetas_paquete = RecetasPorPaquete.objects.filter(paquete=paquete).filter(deleted_at__isnull=True)
    for receta in recetas_paquete:
        # Calcular cantidad a sumar
        cantidad_a_sumar = cantidad * receta.cantidad

        #Verificar si esta receta no es un material de empaquetado
        if receta.receta.material_empaque != None:
            #Como este es un material de empaquetado, no se le agrega a las recetas, si no directo al material
            receta.receta.material_empaque.agregar_inventario(cantidad_a_sumar)

        else:
            # Obtener recetas_inventario para abastecer
            recetas_inventario = RecetaInventario.objects.filter(deleted_at__isnull=True).filter(
                nombre=receta.receta).order_by('-fecha_cad')
            for receta_inventario in recetas_inventario:
                # Verificar que a esta receta_inventario se le pueden quitar de los ocupados
                if receta_inventario.ocupados > 0:
                    if cantidad_a_sumar <= receta_inventario.ocupados:
                        receta_inventario.ocupados-=cantidad_a_sumar
                        receta_inventario.save()
                        break
                    else:
                        cantidad_a_sumar -= receta_inventario.ocupados
                        receta_inventario.ocupados = 0
                        receta_inventario.save()

@group_required('admin')
#Función que devuelve el número de paquetes en inventario para cierto paquete
def obtener_cantidad_inventario(request):
    if request.GET.get('id_paquete'):
        id_paquete = int(request.GET.get('id_paquete'))
        paquete = get_object_or_404(Paquete, pk=id_paquete)
        return HttpResponse("Cantidad en inventario: "+ str(paquete.obtener_disponibles_inventario()))
    else:
        return HttpResponseNotFound()

@group_required('admin')
# Función que devuelve el número de paquetes en inventario para cierto paquete
def obtener_cantidad_inventario_con_caducados(request):
    if request.GET.get('paquete_catalogo'):
        id_paquete = int(request.GET.get('paquete_catalogo'))
        paquete = get_object_or_404(Paquete, pk=id_paquete)
        return HttpResponse("Cantidad en inventario: " + str(paquete.obtener_inventario_fisico()))
    else:
        return HttpResponseNotFound()

@group_required('admin')
# Función que devuelve el número de paquetes en inventario para cierto paquete
def obtener_cantidad_lote(request):
    if request.GET.get('paquete_inventario'):
        id_paquete = int(request.GET.get('paquete_inventario'))
        paquete = get_object_or_404(PaqueteInventario, pk=id_paquete)
        return HttpResponse("Cantidad disponible de este lote: " + str(paquete.disponibles()))
    else:
        return HttpResponseNotFound()

