from django.http import HttpResponseRedirect
from django.urls import reverse

def login_success(request):
    if request.user.groups.filter(name="superuser").exists():
        # Debe ir a ventas
        return HttpResponseRedirect(reverse('paquetes:lista_paquetes'))
    else:
        #A Ordenes porque es administrativo
        return HttpResponseRedirect(reverse('ordenes:ordenes'))
