from django.shortcuts import render,reverse
from .forms import MaterialForm
from .models import Material, MaterialInventario
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum


# Create your views here.

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
        detalle_materiales_en_inventario = MaterialInventario.objects.filter(material_id=id_material, deleted_at__isnull=True)
        response = render_to_string('materiales/lista_detalle_materiales_inventario.html', {'detalle_materiales_en_inventario': detalle_materiales_en_inventario, 'material': material})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')
