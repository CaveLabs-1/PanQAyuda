from django.test import TestCase
from clientes.models import Cliente
from django.urls import reverse

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
