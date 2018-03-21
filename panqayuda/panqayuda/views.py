from django.http import HttpResponseRedirect
from django.urls import reverse

def login_success(request):
    if request.user.groups.filter(name="superuser").exists():
        return HttpResponseRedirect(reverse('paquetes:lista_paquetes')) # Debe ir a ventas
    else:
        return HttpResponseRedirect(reverse('ordenes:ordenes')) #A Ordenes porque es administrativo
