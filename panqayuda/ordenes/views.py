from django.shortcuts import render, get_object_or_404
from recetas.models import Receta, RelacionRecetaMaterial
from .models import Orden
from .forms import FormOrden
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from panqayuda.decorators import group_required
from recetas.models import Receta
from materiales.models import Material

# Lista de ordenes de trabajo y forma para crear una nueva orden de trabajo.
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
            # Filtra la lista de materiales a solo los materiales usados en dicha receta.
            materiales_receta = RelacionRecetaMaterial.objects.filter(receta = receta)
            # Quita el material usado del inventario.
            suficiente = True
            for material_receta in materiales_receta:
                material = Material.object.get(pk = material_receta.material.id)
                if material.obtener_cantidad_inventario() < material_receta.cantidad:
                    suficiente = False
                    break
            if suficiente:
                for material_receta in materiales_receta:
                    materiales_inventario = MaterialInventario.object.filter(material = material).filter(
                        deleted_at__isnull=True).order_by('-fecha_cad')
                    # Calcula la cantidad que se debe restar de dicho material en el inventario.
                    cantidad_a_restar = material_receta.cantidad * multiplicador
                    # Modifica el inventario por recetas, tomando en cuenta la fecha de caducidself.
                    for material_inventario in materiales_inventario:
                        # Si la cantidad disponible de dicho registro es mayor a la cantidad que se necesita restar,
                        # se resta directamente y se termina el proceso.
                        if  material_inventario.cantidad_disponible > cantidad_a_restar:
                            material_inventario.cantidad_disponible -= cantidad
                            material_inventario.save()
                            break
                        else:
                            # En caso de que no exista suficiente material en dicho registro, ocupa todo lo que exite
                            # y pasa al siguiente registro.
                            cantidad_a_restar -= material_inventario.cantidad_disponible
                            material_inventario.cantidad_disponible = 0
                            material_inventario.save()
            else:
                messages.error(request, 'Hubo un error, no hay suficiente material en el inventario.')
                return HttpResponseRedirect(reverse('ordenes:ordenes'))
            # Guarda el registro de la orden de trabajo
            forma_post.save()
            messages.success(request, 'Se ha agregado una nueva orden de trabajo.')
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
        recetas = Receta.objects.filter(deleted_at__isnull=True)
        # Render de la página con la forma vacía y lista de ordenes por entregar.
        tabla = render_to_string('ordenes/tabla_ordenes.html', {'ordenes': ordenes})
        return render(request, 'ordenes/ordenes.html', {'forma': forma, 'ordenes': ordenes, 'recetas':recetas, 'tabla':tabla})


@group_required('admin')
def terminar_orden (request):
    if request.method == 'POST':
         orden= get_object_or_404(Orden, pk=request.POST['id'])
         print(request.POST['id'])
         orden.estatus=request.POST['estatus']
         orden.save()

    ordenes = Orden.ordenes_por_entregar()
    data = render_to_string('ordenes/tabla_ordenes.html', {'ordenes': ordenes})
    return HttpResponse(data)

@group_required('admin')
def cancelar_orden (request):
    if request.method == 'POST':
         orden= get_object_or_404(Orden, pk=request.POST['id'])
         print(request.POST['id'])
         orden.estatus=request.POST['estatus']
         orden.save()

    ordenes = Orden.ordenes_por_entregar()
    data = render_to_string('ordenes/tabla_ordenes.html', {'ordenes': ordenes})
    return HttpResponse(data)
