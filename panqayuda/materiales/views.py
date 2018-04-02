from django.shortcuts import render,reverse
from .forms import MaterialForm
from .models import Material
from django.contrib import messages
from django.http import HttpResponseRedirect


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
