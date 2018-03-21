from django.test import TestCase
from django.urls import reverse
import datetime
from django.shortcuts import render
from clientes.models import Cliente

class TestEditarCliente(TestCase):

    #Existe la vista
    def test_existe_vista(self):
        Cliente.objects.create(id=1, nombre="Bancomer", telefono=4151043944, direccion="calle 100 corazones", rfc=45321343, razon_social="Somos unos cracks", email="ejemplo@hotmail.com")
        resp = self.client.get(reverse('clientes:editar_cliente', kwargs={'id_cliente':1}))
        self.assertEqual(resp.status_code, 200)

    
# Create your tests here.
