from django.test import TestCase
from django.urls import reverse
from ventas.models import Venta
import datetime
from django.contrib.auth.models import User, Group
from django.utils import timezone
from clientes.models import Cliente
from paquetes.models import Paquete, PaqueteInventario
from materiales.models import Material, Unidad, MaterialInventario

class TestListaVentas(TestCase):
# Crea la sesión y los objetos a usarse
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        cliente = Cliente.objects.create(
            nombre="TestLista",
            telefono=4151043944,
            rfc="12342121",
            email="test@ejemplo.com"
        )
        venta = Venta.objects.create(cliente=cliente, monto=1)
        paquete = Paquete.objects.create(nombre="Paquete Test", precio=12344)
        unidad = Unidad.objects.create(nombre="Unidad")
        paqueteinv = PaqueteInventario.objects.create(
            nombre=paquete,
            cantidad=1,
            fecha_cad="2059-03-03 12:31:06-05"
        )


    def test_ac1_Existe_la_vista_de_listado(self):
        resp = self.client.get(reverse('ventas:ventas'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_Muestra_las_ventas_correctas(self):
        self.assertEqual(Venta.objects.count(), 1)
        resp = self.client.get(reverse('ventas:ventas'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['ventas'].count(), 1)
        #self.assertEqual(resp.context['ventas'].cliente, "TestLista")

    def test_ac3_La_vista_detalle_existe(self):
        self.assertEqual(Venta.objects.count(), 1)
        id = Venta.objects.first()
        data = {'id_venta':id.pk}
        resp = self.client.post(reverse('ventas:lista_detalle_venta'), data)
        self.assertEqual(resp.status_code, 200)

    def test_ac4_lista_detalle_es_correcta(self):
        self.assertEqual(Venta.objects.count(), 1)
        id = Venta.objects.first()
        data = {'id_venta':id.pk}
        resp = self.client.post(reverse('ventas:lista_detalle_venta'), data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['venta'].cliente, id.cliente)
# Create your tests here.
