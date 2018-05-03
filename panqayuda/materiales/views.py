from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import MaterialForm, UnidadForm
from .models import Material, MaterialInventario, Unidad
from recetas.models import RecetaInventario, Receta
from paquetes.models import PaqueteInventario, Paquete
from compras.models import Compra
from proveedores.models import Proveedor
from ventas.models import  Venta
from clientes.models import Cliente
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from panqayuda.decorators import group_required
import datetime

@group_required('admin')
def reporte(request):
    materiales = Material.objects.filter(deleted_at__isnull=False)
    paquetes = Paquete.objects.filter(deleted_at__isnull=False)
    recetas = Receta.objects.filter(deleted_at__isnull=False)
    clientes = Cliente.objects.filter(deleted_at__isnull=False)
    compras = Compra.objects.filter(deleted_at__isnull=False)
    ventas = Venta.objects.filter(deleted_at__isnull=False)
    proveedores = Proveedor.objects.filter(deleted_at__isnull=False)



    return render (request, 'materiales/reporte.html', { 'materiales': materiales,
                                    'paquetes': paquetes, 'recetas': recetas,
                                    'clientes': clientes, 'compras': compras,
                                    'ventas': ventas, 'proveedores':proveedores })


"""
    En caso de ser GET regresa una lista de materiales y la forma para agregar un material
"""
@group_required('admin')
def materiales(request):
    # En caso de que exista una petición de tipo POST valida la forma y guarda el material.
    if request.method == 'POST':
        forma_post = MaterialForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            #Verificar si el material es material de empaque
            if request.POST.get('material_empaque'):
                #Crear 'receta' con el mismo nombre que el material de empaque y asociada a este material
                receta = Receta.objects.create(nombre=forma_post.instance.nombre, cantidad=1, duration=timezone.timedelta(days=450000),material_empaque=forma_post.instance)
                receta.save()
            messages.success(request, 'Se ha agregado una nueva materia prima.')
        else:
            # Si no es válida la forma devuelve un mensaje de error.
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')
        return HttpResponseRedirect(reverse('materiales:materiales'))
    else:
        # Genera una nueva forma.
        forma = MaterialForm()
        # Lista de materiales.
        materiales =  Material.objects.filter(deleted_at__isnull=True, status=1)
        # Lista de unidades para los selects.
        unidades = Unidad.objects.filter(deleted_at__isnull=True)
        return render (request, 'materiales/materiales.html', {'forma': forma, 'materiales': materiales, 'unidades': unidades})

"""
    Enlista las unidades existentes
"""
@group_required('admin')
def lista_unidades(request):
    #Si detecta el metodo POST envia la forma y agrega una nueva unidad.
    if request.method == 'POST':
        forma_post = UnidadForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado una nueva unidad.')
        else:
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')
        #Redirige a la vista de unidades.
        return HttpResponseRedirect(reverse('materiales:lista_unidades'))
    else:
        #Renderea el template lista_unidades.html junto con su forma
        forma = UnidadForm()
        unidades =  Unidad.objects.filter(deleted_at__isnull=True)
        return render (request, 'materiales/lista_unidades.html', {'forma': forma, 'unidades': unidades})


"""
    Recibe una unidad y cambia su estatus a 0
"""
@group_required('admin')
def eliminar_unidad(request, id_unidad):
    #Recuperar Unidad
    unidad = get_object_or_404(Unidad, pk=id_unidad)
    unidad.estatus = 0
    #Borrado del objeto
    unidad.deleted_at = timezone.datetime.now()
    unidad.save()
    messages.success(request, '¡Se ha borrado exitosamente la unidad del catálogo!')
    #Regresar a listado de materiales
    return redirect('materiales:lista_unidades')



#Función para borrar una materia prima del catálogo
@group_required('admin')
def eliminar_material(request, id_material):
    #Obtienes la materia primas
    material = get_object_or_404(Material, pk=id_material)
    material.estatus = 0
    #Se hace el borrado
    material.deleted_at = timezone.datetime.now()
    material.save()
    messages.success(request, '¡Se ha borrado exitosamente la materia prima del catálogo!')
    #Regresa a la lista de materiales
    return redirect('materiales:materiales')


"""
    Función que agrega una nueva unidad a la base de datos según la forma, si no tiene
    un POST te regresa la forma para hacerlo
"""
@group_required('admin')
def agregar_unidades(request):
    if request.method == "POST":
        form = UnidadForm(request.POST)
        if form.is_valid():
             unidad = form.save()
             unidad.save()
             messages.success(request, '¡Se ha agregado la unidad al catálogo!')
             return redirect('/materiales/lista_unidades')
        else:
             messages.success(request, '¡Ya hay una unidad con este nombre!')
             return redirect('/materiales/lista_unidades')
    else:
        messages.success(request, '¡Hubo un error con la petición. Inténtalo de nuevo.')
        return redirect('/materiales/lista_unidades')

"""
    Recibe una unidad y cambia los datos a los que fueron recibidos
"""
@group_required('admin')
def modificar_unidad(request, id_unidad):
    #Verifica que exista la unidad que recibe
    unidad = get_object_or_404(Unidad, pk=id_unidad)
    #Si el metodo es POST modifica la unidad correspondiente
    if request.method == "POST":
        form = UnidadForm(request.POST or None, instance=unidad)
        # Valida la forma antes de enviarla
        if form.is_valid():
            unidad = form.save()
            unidad.save
            messages.success(request, '¡Se ha editado la unidad exitosamente!')
            return redirect('materiales:lista_unidades')
        else:
            messages.success(request, 'Ocurrio un error, intenta de nuevo')
            return render(request, 'materiales/modificar_unidad.html', {'form': form, 'unidad': unidad})
    else:
        # Renderea la vista para modificar la unidad con su form
        # correspondiente
        form = UnidadForm()
    return render(request, 'materiales/modificar_unidad.html', {'form': form, 'unidad': unidad})

"""
    Enlista los materiales inevnatrio que existen dentro de los materiales
"""
@group_required('admin')
def lista_materiales_inventario(request):
    materiales=MaterialInventario.objects.filter(deleted_at__isnull=True).filter(estatus=1)
    catalogo_materiales=Material.objects.filter(deleted_at__isnull=True).filter(status=1)

    for catalogo_material in catalogo_materiales:
         aux= MaterialInventario.objects.filter(material_id=catalogo_material.id).filter(deleted_at__isnull=True).aggregate(Sum('porciones_disponible'))
         catalogo_material.total=aux['porciones_disponible__sum'] or 0

    return render(request, 'materiales/lista_materiales_inventario.html', {'materiales':materiales, 'catalogo_materiales':catalogo_materiales})

"""
    Detalla el material inventario
"""
@group_required('admin')
def materiales_por_catalogo(request):
    if request.method == 'POST':
        id_material = request.POST.get('id_material')
        material = Material.objects.get(pk=id_material)
        detalle_materiales_en_inventario = MaterialInventario.objects.filter(material_id=id_material).filter(deleted_at__isnull=True)
        response = render_to_string('materiales/lista_detalle_materiales_inventario.html', {'detalle_materiales_en_inventario': detalle_materiales_en_inventario, 'material': material})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

"""
    Recibe un material y cambia los datos a los que fueron recibidos
"""
@group_required('admin')
def editar_material(request, id_material):
    # Obtener el material a editar.
    material = get_object_or_404(Material, pk=id_material)
    if request.method == "POST":
        # Si el metodo es POST validar la forma y guardar los cambios.
        form = MaterialForm(request.POST or None, instance=material)
        if form.is_valid():
            material = form.save()
            material.save()
            messages.success(request, 'Se ha editado la materia prima exitosamente!')
            return redirect('materiales:materiales')
        else:
            unidades = Unidad.objects.filter(deleted_at__isnull=True)
            return render(request, 'materiales/editar_material.html', {'form': form, 'material': material, 'unidades': unidades})
    form = MaterialForm()
    unidades = Unidad.objects.filter(deleted_at__isnull=True)
    return render(request, 'materiales/editar_material.html', {'form': form, 'material': material, 'unidades': unidades})
