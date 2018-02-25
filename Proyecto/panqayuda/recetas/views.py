from django.shortcuts import render
from django.utils import timezone
from .models import Receta
from .forms import RecetaForm
from django.shortcuts import redirect
#
# # Create your views here.
# def agregar_receta(request):
#     return render(request, 'receta/agregar_receta.html', {})
# def index
from django.http import HttpResponse

def lista_recetas(request):
    template_name = 'lista_recetas.html'
    recetas = list(Receta.objects.all())
    return render(request, 'recetas/lista_recetas.html', {'recetas': recetas})
def agregar_receta(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.save()
            # return redirect('recetas', pk=receta.pk)
    else:
        form = RecetaForm()
    return render(request, 'recetas/agregar_receta.html', {'form': form})
