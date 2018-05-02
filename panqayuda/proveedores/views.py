from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from django.contrib import messages
from materiales.models import Material
from .forms import FormaProveedor
from django.http import HttpResponse, HttpResponseRedirect
from panqayuda.decorators import group_required
import datetime

"""
    Regresa la lista de proovedores con estatus 1 y deleted_at nulo
"""
@group_required('admin')
def lista_proveedores(request):
    lista_proveedores = Proveedor.objects.all().filter(status=1).filter(deleted_at__isnull=True)
    return render(request, 'proveedores/lista_proveedores.html', {'proveedores':lista_proveedores})

"""
    En caso de ser get manda la forma para hacer el post y agregar el proovedor
"""
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

'''
    Editar un proveedor activo.
'''
@group_required('admin')
def editar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
    if request.method == "POST":
        form = FormaProveedor(request.POST or None, instance=proveedor)
        if form.is_valid():
            proveedor = form.save()
            proveedor.save()
            messages.success(request, 'Se ha editado el proveedor exitosamente!')
            return redirect('proveedores:lista_proveedores')
    else:
        form = FormaProveedor()
    return render(request, 'proveedores/editar_proveedor.html', {'form': form, 'proveedor': proveedor})


"""
    Recibe el proovedor y muestra sus detalles en un template aparte
"""
@group_required('admin')
def detallar_proveedor(request, id_proveedor):
        proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
        return render(request, 'proveedores/proveedor.html', {'proveedor': proveedor})


#Función para borrar un proveedor
@group_required('admin')
def eliminar_proveedor(request, id_proveedor):
    #Se obtiene el objeto
    proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
    proveedor.estatus = 0
    #Se borra el  objeto
    proveedor.deleted_at = datetime.datetime.now()
    proveedor.save()
    messages.success(request, '¡Se ha borrado exitosamente el proveedor!')
    #Devuelve a la lista de proveedores
    return redirect('proveedores:lista_proveedores')
