from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from django.contrib import messages
from materiales.models import Material
from .forms import FormaProveedor
from django.http import HttpResponse, HttpResponseRedirect
from panqayuda.decorators import group_required
import datetime

@group_required('admin')
def lista_proveedores(request):
    lista_proveedores = Proveedor.objects.all().filter(status=1).filter(deleted_at__isnull=True)
    return render(request, 'proveedores/lista_proveedores.html', {'proveedores':lista_proveedores})

@group_required('admin')
def agregar_proveedor(request):
    if request.method == "POST":
        form = FormaProveedor(request.POST)
        if form.is_valid():
            proveedor = form.save()
            proveedor.save()
            messages.success(request, 'Se ha agregado la proveedor al catálogo!')
            return redirect('proveedores:detallar_proveedor', id_proveedor=proveedor.id)
        else:
            messages.success(request, 'Hubo un error en la forma!')
            return render(request, 'proveedores/agregar_proveedor.html', {'form': form})
    else:
        form = FormaProveedor()
    return render(request, 'proveedores/agregar_proveedor.html', {'form': form})

@group_required('admin')
def detallar_proveedor(request, id_proveedor):
        proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
        return render(request, 'proveedores/proveedor.html', {'proveedor': proveedor})


#Función para borrar un proveedor @Valter
def eliminar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
    proveedor.estatus = 0
    proveedor.deleted_at = datetime.datetime.now()
    proveedor.save()
    messages.success(request, '¡Se ha borrado exitosamente el proveedor!')
    return redirect('proveedores:lista_proveedores')
