from django.test import TestCase
from clientes.models import Cliente
from django.shortcuts import render
import datetime


class TestEditarCliente(TestCase):

    #Existe la vista
    def test_existe_vista(self):
        Cliente.objects.create(id=1, nombre="Bancomer", telefono=4151043944, rfc=45321343, email="ejemplo@hotmail.com")
        resp = self.client.get(reverse('clientes:editar_cliente', kwargs={'id_cliente':1}))
        self.assertEqual(resp.status_code, 200)

    def test_ac1_se_edita_exitosamente(self):
        #se crea un objeto generico de un cliente
        Cliente.objects.create(id=1, nombre="Bancomer", telefono=4151043944, rfc=45321343, email="ejemplo@hotmail.com")
        self.assertEqual(Cliente.objects.count(), 1)
        #se guarda la informacion que sustituira la del objeto ya creado
        data  = {'nombre':"Banamex", 'telefono':4151043955, 'rfc':456783292, 'email':"ejemplo2@hotmail.com"}
        #se manda con post al editar con ese id la nueva informacion de contacto
        resp = self.client.post(reverse('clientes:editar_cliente', kwargs={'id_cliente':1}), data)
        #se obtiene el objeto nuevamente
        update = Cliente.objects.get(id=1)
        #se checa si el nombre del objeto cambiado es igual a la informacion que se le cambio con el 'data'
        self.assertEqual(update.nombre, "Banamex")

    def test_ac2_no_se_edita_con_campo_nombre_vacio(self):
        #se crea un objeto generico de un cliente
        Cliente.objects.create(id=1, nombre="Bancomer", telefono=4151043944, rfc=45321343, email="ejemplo@hotmail.com")
        first = Cliente.objects.get(id=1)
        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(Cliente.objects.get(id=1).email, "ejemplo@hotmail.com")
        #se guarda la informacion que sustituira la del objeto ya creado
        data  = {'telefono':4151043955, 'rfc':456783292, 'email':"ejemplo2@hotmail.com"}
        resp = self.client.post(reverse('clientes:editar_cliente', kwargs={'id_cliente':1}), data)
        #se obtiene el objeto nuevamente
        update = Cliente.objects.get(id=1)
        self.assertEqual(update.email, "ejemplo@hotmail.com")


# Test agregar cliente US39
class TestAgrergarCliente(TestCase):
    # 39.1 se muestra la lista de clientes.
    def test_existe_vista(self):
        data = {'nombre': 'Alguien', 'telefono': 123654786, 'email':'alguien@algo.com', 'rfc': 'A2345F45DFGRW'}
        self.client.post(reverse('clientes:clientes'), data)
        resp = self.client.get(reverse('clientes:clientes'))
        self.assertEqual(resp.context['clientes'].count(), 1)
        self.assertEqual(resp.status_code, 200)

    # 39.2 es posible agrergar un nuevo cliente con nombre, correo, teléfono y rfc.
    def test_agregar_un_cliente(self):
        self.assertEqual(Cliente.objects.count(), 0)
        data = {'nombre': 'Alguien', 'telefono': 123654786, 'email':'alguien@algo.com', 'rfc': 'A2345F45DFGRW'}
        self.client.post(reverse('clientes:clientes'), data)
        self.assertEqual(Cliente.objects.count(), 1)

    # 39.3 el cliente no se agrega si el falta el campo 'nombre'.
    def test_no_se_agrega_cleinte_si_falta_nombre(self):
        self.assertEqual(Cliente.objects.count(), 0)
        data = {'nombre': '', 'telefono': 123432434, 'email': 'alguien@algo.com', 'rfc': 'A2345F45DFGRW'}
        self.client.post(reverse('clientes:clientes'), data)
        self.assertEqual(Cliente.objects.count(), 0)

    # 39.4 Es posible agregar un nuevo cliente sabiendo, al menos, su nombre.
    def test_se_agrega_cleinte_si_falta_telefono_email_o_rfc(self):
        self.assertEqual(Cliente.objects.count(), 0)
        data = {'nombre': 'prueba', 'telefono': '', 'email': 'alguien@algo.com', 'rfc': 'A2345F45DFGRW'}
        self.client.post(reverse('clientes:clientes'), data)
        self.assertEqual(Cliente.objects.count(), 1)
        data = {'nombre': 'prueba', 'telefono': 123432434, 'email': '', 'rfc': 'A2345F45DFGRW'}
        self.client.post(reverse('clientes:clientes'), data)
        self.assertEqual(Cliente.objects.count(), 2)
        data = {'nombre': 'prueba', 'telefono': 123432434, 'email': 'alguien@algo.com', 'rfc': ''}
        self.client.post(reverse('clientes:clientes'), data)
        self.assertEqual(Cliente.objects.count(), 3)
