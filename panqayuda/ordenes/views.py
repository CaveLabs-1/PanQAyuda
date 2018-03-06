from django.shortcuts import render
from recetas.models import Receta
from .models import Orden
from .forms import FormOrden
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def ordenes (request):
    if request.method == 'POST':
        forma_post = FormOrden(request.POST)
        # date = forma_post
        print (forma_post)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado una nueva orden de trabajo.')
            return HttpResponseRedirect(reverse('ordenes:ordenes'))
        else:
            messages.error(request, 'Hubo un error, intentalo de nuevo')
            return HttpResponseRedirect(reverse('ordenes:ordenes'))

    else:
        forma = FormOrden()
        ordenes = Orden.ordenes_por_entregar()
        recetas = Receta.objects.filter(deleted_at__isnull=True)
        return render(request, 'ordenes/ordenes.html', {'forma': forma, 'ordenes': ordenes, 'recetas':recetas})
