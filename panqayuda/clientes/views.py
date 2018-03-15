from django.shortcuts import render, get_object_or_404
from .models import Cliente
from .forms import FormCliente

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
