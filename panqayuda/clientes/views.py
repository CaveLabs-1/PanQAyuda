from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Cliente
from .forms import FormCliente
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from panqayuda.decorators import group_required
import datetime



@group_required('admin')
# View para mostrar la lista de clientes, con forma disponible para crear un nuevo cliente.
def clientes(request):
    # En caso de que exista una petición de tipo POST significa que se ha intentado dar de alta un nuevo cliente.
    if request.method == 'POST':
        forma_post = FormCliente(request.POST)
        # Si la forma es válida, se guarda el nuevo cliente y devuelve mensaje de éxito.
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado un nuevo cliente.')
        else:
            # De lo contrario devuelve mensaje de error.
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')
        # Sin importar el caso se llama a si misma para pintar la lista de clientes con una nueva forma para dar de alta otro cliente.
        return HttpResponseRedirect(reverse('clientes:clientes'))
    # En caso de que no haya ninguna petición
    else:
        # Se crea una nueva forma para dar de alta un cliente.
        forma = FormCliente()
        # Se obtiene la lista de clientes.
        clientes =  Cliente.objects.filter(deleted_at__isnull=True)
        # Se muestra la lista de clientes con una forma disponible para dar de alta uno nuevo.
        return render (request, 'clientes/clientes.html', {'forma': forma, 'clientes': clientes})

"""
    Recibe el cliente con la información modificada y la asigna al cliente recibido
"""
@group_required('admin')
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    if request.method == "POST":
        form = FormCliente(request.POST or None, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            cliente.save()
            messages.success(request, 'Se ha editado el cliente exitosamente!')
            return redirect('clientes:clientes')
    else:
        form = FormCliente()
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})


#Agregar un cliente desde la vista de ventas y regresar el cliente

def agregar_cliente_venta(request):
    if request.method == 'POST':
        forma_post = FormCliente(request.POST)
        # Si la forma es válida, se guarda el nuevo cliente y devuelve la información necesaria para la vista
        if forma_post.is_valid():
            forma_post.save()
            data = {'nombre':forma_post.instance.nombre, 'val':forma_post.instance.id}
            return JsonResponse(data)
        else:
            print(forma_post.errors)
            # De lo contrario devuelve mensaje de error.
            return HttpResponseNotFound('Hubo un error agregando al cliente, inténtalo de nuevo.')


#Función para borrar un Cliente @Valter
def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    cliente.estatus = 0
    cliente.deleted_at = datetime.datetime.now()
    cliente.save()
    messages.success(request, '¡Se ha borrado exitosamente el cliente!')
    return redirect('clientes:clientes')
