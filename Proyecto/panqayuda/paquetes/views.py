from django.shortcuts import render, get_object_or_404
from .models import Paquete
from .models import Recetas_por_paquete
from recetas.models import Receta
from .forms import FormPaquete, FormRecetasPorPaquete
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse

#indice
def lista_paquetes(request):
    lista_de_paquetes=Paquete.objects.filter(estatus=1)
    return render(request, 'paquetes/lista_paquetes.html', {'paquetes':lista_de_paquetes})

#agregar paquete
def agregar_paquete(request):
    if request.method == 'POST':

        forma_post=FormPaquete(request.POST)
    
        print("before if")
        print(forma_post)
        if forma_post.is_valid():
            print("in if")
            forma_post.save()
            messages.success(request, 'Se ha agregado el paquete al catálogo!')
            paquete = Paquete.objects.latest('id')
            return HttpResponseRedirect(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        else:
            messages.error(request, 'Hubo un error y no se agregó el paquete. Intentalo de nuevo.')
            return HttpResponseRedirect(reverse('paquetes:agregar_paquete'))
    else:
        forma=FormPaquete()
        messages.error(request, ' Esta entrando aqui :( )')
        return render(request, 'paquetes/agregar_paquete.html', {'forma':forma})

#agregar recetas a paquete
def agregar_recetas_a_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, id=id_paquete)
    forma = FormRecetasPorPaquete()
    recetas = Receta.objects.filter(deleted_at__isnull=True, paquete = paquete)
    return render(request, 'paquetes/agregar_recetas_a_paquete.html', {'recetas': recetas, 'forma':forma, 'recetas':recetas})

def agregar_receta_a_paquete(request):
    if request.method == 'POST':
        html = 'hello'
        return HttpResponse(html)

def paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, id=id_paquete)
    recetas = recetas = Receta.objects.filter(deleted_at = null, paquete = paquete)
    return render(request, 'paquetes/paquete.html', {'paquete': paquete, 'recetas': recetas})

# Create your views here.
