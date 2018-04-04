from django.shortcuts import render
from .forms import MaterialForm
from .models import Material
from panqayuda.decorators import group_required


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

# @group_required('admin')
# def unidades(request):
#     if request.method == 'POST':
#         forma_post = FormUnidad(request.POST)
#         if forma_post.is_valid():
#             forma_post.save()
#             messages.success(request, 'Se ha agregado una nueva unidad.')
#         else:
#             messages.error(request, 'Hubo un error, inténtalo de nuevo.')
#
#         return HttpResponseRedirect(reverse('materiales:unidades'))
#     else:
#         forma = FormUnidad()
#         unidades =  Unidad.objects.filter(deleted_at__isnull=True)
#         return render (request, 'materiales/unidades.html', {'forma': forma, 'unidades': unidades})
