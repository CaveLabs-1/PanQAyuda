from django.shortcuts import render, get_object_or_404, redirect
from .models import Paquete
from .models import Recetas_por_paquete
from recetas.models import Receta
from .forms import FormPaquete, FormRecetasPorPaquete
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
import datetime

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


def borrar_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, pk=id_paquete)
    paquete.estatus = 0
    paquete.deleted_at = datetime.datetime.now()
    paquete.save()
    # recetas = list(Receta.objects.filter(status=1))
    messages.success(request, 'Se ha borrado el paquete del catálogo!')
    return redirect('paquetes:lista_paquetes')
    # return render(request, 'recetas/lista_recetas.html', {'recetas': recetas})


def agregar_paquete_inventario(request):
    if request.method == 'POST':
        forma_post=FormPaqueteInventario(request.POST)

        print("entró antes del if")
        print(forma_post)
        if forma_post.is_valid():
            print("entró al if")
            forma_post.save()
            messages.success(request, 'Se ha agregado el paquete al inventario')
            paquete = Paquete_Inventario.objects.latest('id')
            return HttpResponseRedirect(reverse('paquetes:agregar_inventario', kwargs={'nombre':paquete.id}))
        else:
            messages.error(request, 'Hubo un error y no se agregó el paquete al inventario.')
            return HttpResponseRedirect(reverse('paquetes:agregar_inventario'))
    else:
        forma=FormPaqueteInventario()
        messages.error(request, 'Hubo un error con la peticion')
        return render(request, 'placeholder.html', {'forma':forma})

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

def lista_inventario_paquetes(request, id_paquetes):
    inventario = Paquete_Inventario.objects.filter()
    return render(request, 'this is a plaveholder.html', {'inventario':inventario})

#editar paquete
def editar_paquete(request, id_paquete):
    paquete = get_object_or_404(Paquete, pk=id_paquete)
    if request.method == "POST":
        forma = FormPaquete(request.POST or None, instance=paquete)
        if forma.is_valid():
            paquete = forma.save()
            paquete.save
            return HttpResponseRedirect(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
    else:
        forma = FormPaquete(initial={"nombre":paquete.nombre, "precio":paquete.precio})
        return render(request, 'paquetes/editar_paquete.html', {'forma':forma, 'paquete':paquete})