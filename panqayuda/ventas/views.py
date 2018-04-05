from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import VentaForm
from .models import Venta
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from panqayuda.decorators import group_required
import datetime


def ventas(request):
    if request.method == 'POST':
        forma_post = VentaForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado una nueva venta.')
        else:
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')

        return HttpResponseRedirect(reverse('ventas:ventas'))
    else:
        forma = VentaForm()
        ventas =  Venta.objects.filter(deleted_at__isnull=True)
        return render (request, 'ventas/ventas.html', {'forma': forma, 'ventas': ventas})
