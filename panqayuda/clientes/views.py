from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente
from .forms import FormCliente
from django.contrib import messages

def clientes(request):
    if request.method == 'POST':
        forma_post = FormCliente(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            message.success(request, 'Se ha agregado un nuevo cliente.')
        else:
            message.error(request, 'Hubo un error, intentalo de nuevo.')

        return HttpResponseRedirect(reverse('clientes:clientes'))
    else:
        forma = FormCliente()
        clientes =  Cliente.objects.filter(deleted_at__isnull=True)
        return render (request, 'clientes/clientes.html', {'forma': forma, 'clientes': clientes})


def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    if request.method == "POST":
        form = FormCliente(request.POST or None, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            cliente.save
            messages.success(request, 'Se ha editado el cliente exitosamente!')
            return redirect('clientes:clientes')
    else:
        form = FormCliente()
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})
