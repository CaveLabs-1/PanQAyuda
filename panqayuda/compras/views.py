from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import CompraForm
from materiales.forms import MaterialInventarioForm
from proveedores.models import Proveedor
from .models import Compra
from materiales.models import Material, MaterialInventario, Unidad
from materiales.forms import MaterialInventarioForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.db.models import Sum
from panqayuda.decorators import group_required
from django.utils import timezone

"""
    Función que enlista las compras y permite agregar una compra a la base de datos.
"""
@group_required('admin')
def compras(request):
    compras =  Compra.objects.all()
    return render (request, 'compras/compras.html', {'compras': compras})


""" --------------------------------------------------
 Reccibe el ID de una compra, obtiene todos los materiales que le
 corresponden y los regresa a la vista
--------------------------------------------------
"""
@group_required('admin')
def lista_detalle_compra(request):
    if request.method == 'POST':
        id_compra = request.POST.get('id_compra')
        #recuperar compra
        compra = Compra.objects.get(pk=id_compra)
        #obtener los material inventario que pertenecen a esa compra
        materiales_de_compra = MaterialInventario.objects.filter(compra=compra)
        #obtener html que se insertará al modal
        response = render_to_string('compras/lista_detalle_compra.html', {'materiales_de_compra': materiales_de_compra, 'compra': compra})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

"""
    Función que agrega una compra a la base de datos.
"""
@group_required('admin')
def agregar_compra(request):
    if request.method == 'POST':
        forma = CompraForm(request.POST)
        #revisar que la forma sea válida
        if forma.is_valid():
            forma.save()
            #mensaje de éxito
            messages.success(request, '¡Se ha agregado una compra!')
            compra = Compra.objects.latest('id')
            return HttpResponseRedirect(reverse('compras:agregar_materias_primas_a_compra', kwargs={'id_compra':compra.id}))
        else:
            #mensaje de error
            messages.error(request, 'Hubo un error y no se agregó la compra. Inténtalo de nuevo.')
    #recuperar proveedores activos
    proveedores = Proveedor.objects.filter(deleted_at__isnull=True);
    forma = CompraForm()
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
     unidades = Unidad.objects.filter(deleted_at__isnull=True)
     materia_primas = Material.objects.filter(deleted_at__isnull=True)
     formahtml = render_to_string('compras/forma_agregar_compra.html', {'materia_primas':materia_primas, 'unidades':unidades, 'id_compra':id_compra, 'forma':forma})

     #generar lista_materia_prima_por_compra
     materias_primas_de_compra = MaterialInventario.objects.filter(compra=compra).filter(deleted_at__isnull=True)
     aux= MaterialInventario.objects.filter(compra_id=id_compra).filter(deleted_at__isnull=True).aggregate(Sum('costo'))
     total=aux['costo__sum']
     lista_materia_prima_por_compra = render_to_string('compras/lista_materia_prima_por_compra.html', {'materias_primas_de_compra':materias_primas_de_compra, 'total': total})

     return render (request, 'compras/agregar_materias_primas_a_compra.html', {'formahtml':formahtml, 'lista_materia_prima_por_compra':lista_materia_prima_por_compra})

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
            materia_prima = get_object_or_404(Material, id=id_material)
            fecha_cad= request.POST.get('fecha_cad')
            cantidad = float(request.POST.get('cantidad'))
            id_unidad = materia_prima.unidad_entrada.id
            porciones = cantidad * materia_prima.equivale_maestra / materia_prima.equivale_entrada
            costo = float(request.POST.get('costo'))
            costo_unitario = float(request.POST.get('costo'))/porciones
            id_compra =  request.POST.get('compra')

            compra = get_object_or_404(Compra, id=id_compra)
            unidad = get_object_or_404(Unidad, id=id_unidad)

            #Dar de alta material inventario
            MaterialInventario.objects.create(material=materia_prima, fecha_cad=fecha_cad, cantidad=cantidad,
             porciones_disponible=porciones, unidad_entrada=unidad, porciones=porciones,
             costo=costo, compra=compra, costo_unitario=costo_unitario )

            #generar forma html
            forma = MaterialInventarioForm()
            unidades = Unidad.objects.filter(deleted_at__isnull=True)
            materia_primas = Material.objects.filter(deleted_at__isnull=True)
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




#Función para borrar una compra
@group_required('admin')
def eliminar_compra(request, id_compra):
    #Se obtiene el objeto compra
    compra = get_object_or_404(Compra, pk=id_compra)

    #Se verifica que los materiales inventarios que están asociados a esta compra no hayan sido ya ocupados
    materiales_compra = compra.materialinventario_set.all()

    for material_compra in materiales_compra:
        #Verificar que no se hayan utilizado porciones de este material inventario
        if material_compra.porciones_disponible != material_compra.porciones:
            messages.error(request, "No se ha podido cancelar la compra porque algunos de las materias primas que se compraron ya han sido utilizadas en producción.")
            return redirect('compras:compras')

    #Eliminar los materiales inventario de esta compra
    for material_compra in materiales_compra:
        material_compra.deleted_at= timezone.now()
        material_compra.save()
    compra.estatus = 0
    #Se borra la compra
    compra.deleted_at = timezone.now()
    compra.save()
    messages.success(request, '¡Se ha cancelado exitosamente la compra!')
    #Se regresa a la lista de compras
    return redirect('compras:compras')
