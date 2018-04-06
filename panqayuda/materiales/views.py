from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import MaterialForm, UnidadForm
from .models import Material, MaterialInventario, Unidad
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from panqayuda.decorators import group_required
import datetime


# Create your views here.

@group_required('admin')
def materiales(request):
    if request.method == 'POST':
        forma_post = MaterialForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado un nuevo material.')
        else:
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')

        return HttpResponseRedirect(reverse('materiales:materiales'))
    else:
        forma = MaterialForm()
        materiales =  Material.objects.filter(deleted_at__isnull=True)
        return render (request, 'materiales/materiales.html', {'forma': forma, 'materiales': materiales})

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
        messages.success(request, '¡Hubo un error con el POST!')
        return redirect('/materiales/lista_unidades')

def lista_materiales_inventario(request):
    materiales=MaterialInventario.objects.filter(deleted_at__isnull=True).filter(estatus=1)
    catalogo_materiales=Material.objects.filter(deleted_at__isnull=True).filter(status=1)

    for catalogo_material in catalogo_materiales:
         aux= MaterialInventario.objects.filter(material_id=catalogo_material.id).filter(deleted_at__isnull=True).aggregate(Sum('cantidad'))
         catalogo_material.total=aux['cantidad__sum']

    return render(request, 'materiales/lista_materiales_inventario.html', {'materiales':materiales, 'catalogo_materiales':catalogo_materiales})

def materiales_por_catalogo(request):
    if request.method == 'POST':
        id_material = request.POST.get('id_material')
        material = Material.objects.get(pk=id_material)
        detalle_materiales_en_inventario = MaterialInventario.objects.filter(material_id=id_material).filter(deleted_at__isnull=True)
        #print(detalle_materiales_en_inventario)
        response = render_to_string('materiales/lista_detalle_materiales_inventario.html', {'detalle_materiales_en_inventario': detalle_materiales_en_inventario, 'material': material})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

def editar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    if request.method == "POST":
        form = MaterialForm(request.POST or None, instance=material)
        if form.is_valid():
            material = form.save()
            material.save
            messages.success(request, 'Se ha editado la material exitosamente!')
            return redirect('materiales:materiales')
    else:
        form = MaterialForm()
    return render(request, 'materiales/editar_material.html', {'form': form, 'material': material})
