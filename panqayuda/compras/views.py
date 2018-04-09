from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import CompraForm
from .models import Compra, RelacionCompraMaterial
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from panqayuda.decorators import group_required
import datetime

# Create your views here.

def compras(request):
    if request.method == 'POST':
        forma_post = CompraForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado una nueva compra.')
        else:
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')

        return HttpResponseRedirect(reverse('compras:compras'))
    else:
        forma = CompraForm()
        compras =  Compra.objects.filter(deleted_at__isnull=True)
        return render (request, 'compras/compras.html', {'forma': forma, 'compras': compras})


def lista_detalle_compra(request):
    if request.method == 'POST':
        id_compra = request.POST.get('id_compra')
        compra = Compra.objects.get(pk=id_compra)
        materiales_de_compra = RelacionCompraMaterial.objects.filter(compra=compra)
        response = render_to_string('compras/lista_detalle_compra.html', {'materiales_de_compra': materiales_de_compra, 'compra': compra})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')
