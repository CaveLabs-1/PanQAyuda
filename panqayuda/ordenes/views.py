from django.shortcuts import render, get_object_or_404
from recetas.models import Receta
from .models import Orden
from .forms import FormOrden
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from panqayuda.decorators import group_required
from django.contrib.auth.decorators import login_required

# Lista de ordenes de trabajo y forma para crear una nueva orden de trabajo.
@login_required
@group_required('admin')
def ordenes (request):
    # En caso de que la petición sea tipo 'POST' crea la forma con los datos obtenidos y la valida.
    if request.method == 'POST':
        forma_post = FormOrden(request.POST)
        if forma_post.is_valid():
            # Si la forma es valida, guarda el registro y devuelve mensaje de éxito.
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
