from django.shortcuts import render
#
# # Create your views here.
# def agregar_receta(request):
#     return render(request, 'receta/agregar_receta.html', {})
# def index
from django.http import HttpResponse

def recetas_list(request):
    return render(request, 'recetas/recetas_list.html', {})
