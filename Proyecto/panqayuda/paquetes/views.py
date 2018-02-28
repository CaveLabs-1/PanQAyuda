from django.shortcuts import render
from .models import Paquete
from .models import Recetas_por_paquete
from recetas.models import Receta
from .forms import FormPaquete, FormRecetasPorPaquete



#indice
def lista_paquetes(request):
    lista_de_paquetes=Paquete.objects.filter(estatus=1)
    return render(request, 'paquetes/lista_paquetes.html', {'paquetes':lista_de_paquetes})

#agregar paquete
def agregar_paquete(request):
    if request.method == 'POST':
        forma_post=FormPaquete(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha agregado el paquete al catálogo!')
        else:
            message.error(request, 'Hubo un error, no se agregó el paquete.')
        return render(request, 'paquetes/agregar_paquete.html', forma_post)
    else:
        forma=FormPaquete()
        return render(request, 'paquetes/agregar_paquete.html', forma)

#agregar recetas a paquete
def agregar_recetas_a_paquete():
    return render(request, 'paquetes/agregar_recetas_a_paquete.html')

#detalle de paquete
def paquete():
    return render(request, 'paquetes/paquete.html')

# Create your views here.
