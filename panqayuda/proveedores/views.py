from django.shortcuts import render
from .models import Proveedor

def lista_proveedores(request):
    lista_proveedores = Proveedor.objects.all().filter(status=1).filter(deleted_at__isnull=True)
    return render('lista_proveedores.html', {'proveedores':lista_proveedores})