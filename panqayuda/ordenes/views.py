from django.shortcuts import render, get_object_or_404
from recetas.models import Receta, RelacionRecetaMaterial, RecetaInventario
from .models import Orden
from .forms import FormOrden
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from panqayuda.decorators import group_required
from recetas.models import Receta
from django.utils import timezone
from materiales.models import Material, MaterialInventario, Unidad
from django.db.models import F
import datetime
'''
    Lista de odenes de trabajo, con forma para dar de alta una nueva orden de trbajo.
    En caso de que se de de alta una nueva orden de trabajo, se descuenta el material
    que esta ocupa.
'''
@group_required('admin')
def ordenes (request):
    # En caso de que la petición sea tipo 'POST' crea la forma con los datos obtenidos y la valida.
    if request.method == 'POST':
        forma_post = FormOrden(request.POST)
        # Si la forma es valida, guarda el registro y devuelve mensaje de éxito.
        if forma_post.is_valid():
            # Obtiene los datos de la forma.
            data = forma_post.cleaned_data
            # Guarda el registro de la receta seleccionada en una variable.
            receta = data['receta']
            # Guarda el multiplicador en una variable
            multiplicador = data['multiplicador']

            # No permite que el multiplicador sea menor o igaul a 0
            if multiplicador < 1 :
                messages.error(request, 'Hubo un error, no es posible agregar una orden de trabajo con multiplicador menor a 1')
                return HttpResponseRedirect(reverse('ordenes:ordenes'))

            # Filtra la lista de materiales a solo los materiales usados en dicha receta.
            materiales_receta = RelacionRecetaMaterial.objects.filter(receta = receta)

            # En caso de que no exista material suficiente en el invenario no permite generar la orden de trabajo.
            for material_receta in materiales_receta:
                material = Material.objects.get(pk = material_receta.material.id)
                if material.obtener_cantidad_inventario() < material_receta.cantidad * multiplicador:
                    messages.error(request, 'Hubo un error, no hay suficiente '+ material.nombre +' en el inventario.')
                    return HttpResponseRedirect(reverse('ordenes:ordenes'))

            # Quita el material usado del inventario.
            costo=0
            materiales_receta = RelacionRecetaMaterial.objects.filter(receta = receta)
            for material_receta in materiales_receta:
                materiales_inventario = MaterialInventario.objects.filter(material = material_receta.material).filter(
                    fecha_cad__gte=timezone.now(),deleted_at__isnull=True).order_by('fecha_cad')
                # Calcula la cantidad que se debe restar de dicho material en el inventario.
                cantidad_a_restar = float(material_receta.cantidad * multiplicador)
                cantidad_a_restar_inicial = cantidad_a_restar
                # Modifica el inventario por recetas, tomando en cuenta la fecha de caducidself.
                for material_inventario in materiales_inventario:
                    # Si la cantidad disponible de dicho registro es mayor a la cantidad que se necesita restar,
                    # se resta directamente y se termina el proceso.
                    if  material_inventario.porciones_disponible > cantidad_a_restar:
                        material_inventario.porciones_disponible -= cantidad_a_restar
                        material_inventario.save()
                        costo+= (material_inventario.costo_unitario * cantidad_a_restar)/cantidad_a_restar_inicial
                        break
                    else:
                        # En caso de que no exista suficiente material en dicho registro, ocupa todo lo que existe
                        # y pasa al siguiente registro.
                        costo+=(material_inventario.costo_unitario * material_inventario.porciones_disponible)/cantidad_a_restar_inicial
                        cantidad_a_restar -= (material_inventario.porciones_disponible)
                        material_inventario.porciones_disponible = 0
                        material_inventario.save()

            Orden.objects.create(receta=data['receta'], multiplicador=data['multiplicador'], fecha_fin=data['fecha_fin'], costo=costo)
            messages.success(request, 'Se ha agregado una nueva orden de trabajo.')
            # Guarda el registro de la orden de trabajo
            return HttpResponseRedirect(reverse('ordenes:ordenes'))
        else:
            # Si la forma no es valida, devuelve mensaje de error y recarga la página.
            messages.error(request, 'Hubo un error, intentalo de nuevo.')
            return HttpResponseRedirect(reverse('ordenes:ordenes'))
    #En caso de que no haya ninguna petición, crea la forma vacía y carga la lista de ordenes por entregar.
    else:
        forma = FormOrden()
        # Filtrar ordenes qeu están por entregar.
        ordenes = Orden.ordenes_por_entregar()
        # Listas de recetas para genrar el select.
        recetas = Receta.objects_sin_empaquetado.filter(deleted_at__isnull=True)
        # Render de la página con la forma vacía y lista de ordenes por entregar.
        tabla = render_to_string('ordenes/tabla_ordenes.html', {'ordenes': ordenes})
        ordenes = Orden.objects.all()
        tabla_historial = render_to_string('ordenes/tabla_ordenes_historial.html', {'ordenes': ordenes})
        return render(request, 'ordenes/ordenes.html', {'forma': forma, 'tabla_historial':tabla_historial, 'recetas':recetas, 'tabla':tabla})

'''
    Cuando una orden de trabajo se marca como terminada, se agrega las recetas que
    esta generó al inventario.
'''
@group_required('admin')
def terminar_orden (request):
    if request.method == 'POST':
         orden= get_object_or_404(Orden, pk=request.POST['id'])
         if orden.estatus == '1':
             orden.estatus=request.POST['estatus']
             total_creadas = orden.receta.cantidad * orden.multiplicador
             RecetaInventario.objects.create(nombre = orden.receta, cantidad = total_creadas, fecha_cad = (timezone.now() + orden.receta.duration), costo= orden.costo)
             orden.save()
    ordenes = Orden.ordenes_por_entregar()
    data = render_to_string('ordenes/tabla_ordenes.html', {'ordenes': ordenes})
    return HttpResponse(data)

'''
    Si se cancela una orden de trabajo se cambia el estatus de esta y desaparece
    de la lista.
'''
@group_required('admin')
def cancelar_orden (request):
    if request.method == 'POST':
         orden= get_object_or_404(Orden, pk=request.POST['id'])
         orden.estatus=request.POST['estatus']
         #Reabastecer el inventario y el producto semiterminado
         cantidad_a_sumar = orden.cantidad()
         receta = orden.receta
         cancelar_orden_reabastecer_material(receta,cantidad_a_sumar)
         orden.save()

    ordenes = Orden.ordenes_por_entregar()
    data = render_to_string('ordenes/tabla_ordenes.html', {'ordenes': ordenes})
    return HttpResponse(data)

#Cuando se cancela una orden de trabajo, el inventario de materias primas se reabastece
def cancelar_orden_reabastecer_material(receta,cantidad):
    #Obtener las relaciones de la receta
    relaciones_receta = RelacionRecetaMaterial.objects.filter(receta=receta)
    for relacion_receta in relaciones_receta:
        #Calcular cantidad a reabastecer
        cantidad_a_sumar = float(cantidad * relacion_receta.cantidad)

        #Obtener los materiales inventario de cada relacion, excluyendo a los que no pueden recibir y a los eliminados
        material = relacion_receta.material
        materiales_inventario = MaterialInventario.objects.filter(material=material,deleted_at__isnull=True, porciones_disponible__lt=F('porciones')).order_by('-fecha_cad')

        #Abastecer materiales inventario hasta que la cantidad a sumar sea 0
        for material_inventario in materiales_inventario:
            #Este material inventario no puede recibirlo todo
            if cantidad_a_sumar > (material_inventario.porciones - material_inventario.porciones_disponible):
                cantidad_a_sumar -= (material_inventario.porciones - material_inventario.porciones_disponible)
                material_inventario.porciones_disponible = material_inventario.porciones
                material_inventario.save()
            else:
            #Este material inventario puede recibirlo todo
                material_inventario.porciones_disponible += cantidad_a_sumar
                material_inventario.save()
                break
