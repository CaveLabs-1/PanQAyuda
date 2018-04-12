from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import CompraForm
from .models import Compra
from materiales.models import MaterialInventario
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from panqayuda.decorators import group_required
import datetime


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
        materiales_de_compra = MaterialInventario.objects.filter(compra=compra)
        response = render_to_string('compras/lista_detalle_compra.html', {'materiales_de_compra': materiales_de_compra, 'compra': compra})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

"""
    Función que agrega una compra a la base de datos.
"""
@group_required('admin')
def agregar_compra(request):
    if request.method == 'POST':
        forma=CompraForm(request.POST)
        if forma.is_valid():
            forma.save()
            messages.success(request, '¡Se ha agregado una compra!')
            compra = Compra.objects.latest('id')
            return HttpResponseRedirect(reverse('compras:agregar_materias_primas_a_compra', kwargs={'id_compra':compra.id}))
        else:
            messages.error(request, 'Hubo un error y no se agregó la compra. Inténtalo de nuevo.')
    proveedores = Proveedor.objects.filter(deleted_at__isnull=True);
    forma=CompraForm()
    return render(request, 'compras/agregar_compra.html', {'forma':forma, 'proveedores':proveedores})

"""
    Función que regresa template para agregar materias primas a una compra
"""
@group_required('admin')
def agregar_materias_primas_a_compra(request, id_compra):
     compra = get_object_or_404(Compra, id=id_compra)
     #Checar que sea una compra activa
     if compra.deleted_at != None:
         raise Http404

     #generar forma html
     forma = MaterialInventarioForm()
     unidades = Unidad.objects.filter(deleted_at__isnull=True);
     materia_primas = Material.objects.filter(deleted_at__isnull=True);
     formahtml = render_to_string('compras/forma_agregar_compra.html', {'materia_primas':materia_primas, 'unidades':unidades, 'id_compra':id_compra, 'forma':forma})

     #generar lista_materia_prima_por_compra
     materias_primas_de_compra = MaterialInventario.objects.filter(compra=compra).filter(deleted_at__isnull=True)
     aux= MaterialInventario.objects.filter(compra_id=id_compra).filter(deleted_at__isnull=True).aggregate(Sum('costo'))
     total=aux['costo__sum']
     lista_materia_prima_por_compra = render_to_string('compras/lista_materia_prima_por_compra.html', {'materias_primas_de_compra':materias_primas_de_compra, 'total': total});

     return render (request, 'compras/agregar_materias_primas_a_compra.html', {'formahtml':formahtml, 'lista_materia_prima_por_compra':lista_materia_prima_por_compra});

"""
    Función agrega materias primas a una compra
"""
@group_required('admin')
def agregar_materia_prima_a_compra(request):
    if request.method == 'POST':
        forma = MaterialInventarioForm(request.POST)
        if forma.is_valid():
            #Recuperar datos de AJAX
            id_material = int(request.POST.get('material'))
            fecha_cad= request.POST.get('fecha_cad')
            cantidad = int(request.POST.get('cantidad'))
            id_unidad = int(request.POST.get('unidad_entrada'))
            porciones = int(request.POST.get('porciones'))
            costo = int(request.POST.get('costo'))
            id_compra =  request.POST.get('compra')

            materia_prima = get_object_or_404(Material, id=id_material)
            compra = get_object_or_404(Compra, id=id_compra)
            unidad = get_object_or_404(Unidad, id=id_unidad)

            #Dar de alta material inventario
            MaterialInventario.objects.create(material=materia_prima, fecha_cad=fecha_cad, cantidad=cantidad,
             cantidad_disponible=cantidad, unidad_entrada=unidad, porciones=porciones,
             costo=costo, compra=compra )

            #generar forma html
            forma = MaterialInventarioForm()
            unidades = Unidad.objects.filter(deleted_at__isnull=True);
            materia_primas = Material.objects.filter(deleted_at__isnull=True);
            formahtml = render_to_string('compras/forma_agregar_compra.html', {'materia_primas':materia_primas, 'unidades':unidades, 'id_compra':id_compra, 'forma':forma})

            #generar lista_materia_prima_por_compra
            materias_primas_de_compra = MaterialInventario.objects.filter(compra=compra).filter(deleted_at__isnull=True)
            aux= MaterialInventario.objects.filter(compra_id=id_compra).filter(deleted_at__isnull=True).aggregate(Sum('costo'))
            total=aux['costo__sum']
            lista_materia_prima_por_compra = render_to_string('compras/lista_materia_prima_por_compra.html', {'materias_primas_de_compra':materias_primas_de_compra, 'total':total});

            #concatenar formahtml y lista_materia_prima_por_compra
            data = '' + formahtml + lista_materia_prima_por_compra + ''
            #regresar a AJAX
            return HttpResponse(data)
        else:
            mensaje_error = ""
            for field,errors in forma.errors.items():
                 for error in errors:
                     mensaje_error+=error + "\n"
            return HttpResponseNotFound('Hubo un problema agregando la materia prima a la compra: '+ mensaje_error)
