from django.shortcuts import render
from django.http import request

def prueba_view(request):
    return render(request, 'prueba/prueba.html')


# Create your views here.
