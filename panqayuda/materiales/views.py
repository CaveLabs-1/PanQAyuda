from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import MaterialForm, UnidadForm
from .models import Material, MaterialInventario, Unidad
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from panqayuda.decorators import group_required
import datetime


# Lista de materiales con modal para dar de alta uno nuevo.
@group_required('admin')
def materiales(request):
    # En caso de que exista una petición de tipo POST valida la forma y guarda el material.
    if request.method == 'POST':
        forma_post = MaterialForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado un nuevo material.')
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

@group_required('admin')
def lista_unidades(request):
    if request.method == 'POST':
        forma_post = UnidadForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado una nueva unidad.')
        else:
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')

        return HttpResponseRedirect(reverse('materiales:lista_unidades'))
    else:
        forma = UnidadForm()
        unidades =  Unidad.objects.filter(deleted_at__isnull=True)
        return render (request, 'materiales/lista_unidades.html', {'forma': forma, 'unidades': unidades})




def eliminar_unidad(request, id_unidad):
    unidad = get_object_or_404(Unidad, pk=id_unidad)
    unidad.estatus = 0
    unidad.deleted_at = datetime.datetime.now()
    unidad.save()
    messages.success(request, '¡Se ha borrado exitosamente la unidad del catálogo!')
    return redirect('materiales:lista_unidades')


#Función para borrar una materia prima @Valter
def eliminar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    material.estatus = 0
    material.deleted_at = datetime.datetime.now()
    material.save()
    messages.success(request, '¡Se ha borrado exitosamente el material del catálogo!')
    return redirect('materiales:materiales')


"""
    Función que agrega una nueva unidad a la base de datos según la forma, si no tiene
    un POST te regresa la forma para hacerlo
"""
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
        messages.success(request, '¡Hubo un error con el POST!')
        return redirect('/materiales/lista_unidades')

@group_required('admin')
def modificar_unidad(request, id_unidad):
    unidad = get_object_or_404(Unidad, pk=id_unidad)
    if request.method == "POST":
        form = UnidadForm(request.POST or None, instance=unidad)
        if form.is_valid():
            unidad = form.save()
            unidad.save
            messages.success(request, '¡Se ha editado la unidad exitosamente!')
            return redirect('materiales:lista_unidades')
        else:
            messages.success(request, 'Ocurrio un error, intenta de nuevo')
            return render(request, 'materiales/modificar_unidad.html', {'form': form, 'unidad': unidad})
    else:
        form = UnidadForm()
    return render(request, 'materiales/modificar_unidad.html', {'form': form, 'unidad': unidad})

@group_required('admin')
def lista_materiales_inventario(request):
    materiales=MaterialInventario.objects.filter(deleted_at__isnull=True).filter(estatus=1)
    catalogo_materiales=Material.objects.filter(deleted_at__isnull=True).filter(status=1)

    for catalogo_material in catalogo_materiales:
         aux= MaterialInventario.objects.filter(material_id=catalogo_material.id).filter(deleted_at__isnull=True).aggregate(Sum('cantidad'))
         catalogo_material.total=aux['cantidad__sum']

    return render(request, 'materiales/lista_materiales_inventario.html', {'materiales':materiales, 'catalogo_materiales':catalogo_materiales})

@group_required('admin')
def materiales_por_catalogo(request):
    if request.method == 'POST':
        id_material = request.POST.get('id_material')
        material = Material.objects.get(pk=id_material)
        detalle_materiales_en_inventario = MaterialInventario.objects.filter(material_id=id_material).filter(deleted_at__isnull=True)
        #print(detalle_materiales_en_inventario)
        response = render_to_string('materiales/lista_detalle_materiales_inventario.html', {'detalle_materiales_en_inventario': detalle_materiales_en_inventario, 'material': material})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

@group_required('admin')
def editar_material(request, id_material):
    # Obtener el material a editar.
    material = get_object_or_404(Material, pk=id_material)
    if request.method == "POST":
        # Si el metodo es POST validar la forma y guardar los cambios.
        form = MaterialForm(request.POST or None, instance=material)
        if form.is_valid():
            material = form.save()
            material.save
            messages.success(request, 'Se ha editado el material exitosamente!')
            return redirect('materiales:materiales')
    form = MaterialForm()
    unidades = Unidad.objects.filter(deleted_at__isnull=True)
    return render(request, 'materiales/editar_material.html', {'form': form, 'material': material, 'unidades': unidades})
