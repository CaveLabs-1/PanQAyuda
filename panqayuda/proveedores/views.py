from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from django.contrib import messages
from materiales.models import Material
from .forms import FormaProveedor
from django.http import HttpResponse, HttpResponseRedirect
import datetime

def lista_proveedores(request):
    lista_proveedores = Proveedor.objects.all().filter(status=1).filter(deleted_at__isnull=True)
    return render('lista_proveedores.html', {'proveedores':lista_proveedores})


def agregar_proveedor(request):
    if request.method == "POST":
        form = FormaProveedor(request.POST)
        if form.is_valid():
            proveedor = form.save()
            proveedor.save()
            messages.success(request, 'Se ha agregado la proveedor al catálogo!')
            return redirect('proveedores:lista_proveedores', id_proveedor=proveedor.id)
        else:

            messages.success(request, 'Hubo un error en la forma!')
            return render(request, 'proveedores/agregar_proveedor.html', {'form': form})
    else:
        form = FormaProveedor()
    return render(request, 'proveedores/agregar_proveedor.html', {'form': form})
