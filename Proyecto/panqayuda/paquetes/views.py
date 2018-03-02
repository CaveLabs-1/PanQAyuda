from django.shortcuts import render, get_object_or_404
from .models import Paquete
from .models import Recetas_por_paquete
from recetas.models import Receta
from .forms import FormPaquete, FormRecetasPorPaquete
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string

#indice
def lista_paquetes(request):
    lista_de_paquetes=Paquete.objects.filter(estatus=1)
    return render(request, 'paquetes/ver_paquetes.html', {'paquetes':lista_de_paquetes})

#agregar paquete
def agregar_paquete(request):
    if request.method == 'POST':
        forma_post=FormPaquete(request.POST)
        if forma_post.is_valid():
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
    recetas_por_paquete = Recetas_por_paquete.objects.filter(paquete=paquete)
    recetas = Receta.objects.filter(deleted_at__isnull=True)
    formahtml = render_to_string('paquetes/forma_agregar_recetas_paquete.html', {'forma': forma, 'recetas': recetas, 'paquete': paquete})
    lista_recetas = render_to_string('paquetes/lista_recetas_por_paquete.html', {'recetas_por_paquete': recetas_por_paquete})
    return render(request, 'paquetes/agregar_recetas_a_paquete.html', {'formahtml': formahtml, 'lista_recetas':lista_recetas, 'recetas': recetas, 'paquete': paquete, 'forma': forma})

def agregar_receta_a_paquete(request):
    if request.method == 'POST':
        id_receta = int(request.POST.get('receta'))
        receta = get_object_or_404(Receta, id = id_receta)
        cantidad = int(request.POST.get('cantidad'))
        id_paquete = int(request.POST.get('paquete'))
        paquete = get_object_or_404(Paquete, id = id_paquete)
        Recetas_por_paquete.objects.create(paquete = paquete,receta = receta, cantidad= cantidad )
        forma = FormRecetasPorPaquete()
        recetas_por_paquete = Recetas_por_paquete.objects.filter(paquete = paquete)
        recetas = Receta.objects.filter(deleted_at__isnull=True)
        formahtml = render_to_string('paquetes/forma_agregar_recetas_paquete.html', {'forma': forma, 'recetas': recetas, 'paquete': paquete})
        lista_recetas = render_to_string('paquetes/lista_recetas_por_paquete.html', {'recetas_por_paquete': recetas_por_paquete})
        data = ''+formahtml + lista_recetas+''
        return HttpResponse(data)

def paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, id=id_paquete)
    recetas = recetas = Receta.objects.filter(deleted_at = null, paquete = paquete)
    return render(request, 'paquetes/paquete.html', {'paquete': paquete, 'recetas': recetas})

# Create your views here.
