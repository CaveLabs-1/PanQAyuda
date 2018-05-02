from django.test import TestCase
from django.urls import reverse
from ventas.models import Venta, RelacionVentaPaquete
import datetime
from django.contrib.auth.models import User, Group
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
        venta = Venta.objects.create(cliente=cliente, monto_total=1)
        paquete = Paquete.objects.create(nombre="Paquete Test", precio=12344)
        unidad = Unidad.objects.create(nombre="Unidad")
        paqueteinv = PaqueteInventario.objects.create(
            nombre=paquete,
            cantidad=1,
            fecha_cad=datetime.date(2038, 3, 31)
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

'''
    US38 Cancelar venta
    Probar que es posible cancelar una venta y que el inventario se actualice
    cuando esto pase.
'''
class TestCancelarVenta(TestCase):
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
        venta = Venta.objects.create(cliente=cliente, monto_total=180)
        paquete = Paquete.objects.create(nombre="Paquete Test", precio=60)
        unidad = Unidad.objects.create(nombre="Unidad")
        paqueteinv = PaqueteInventario.objects.create(
            nombre=paquete,
            cantidad=10,
            ocupados=3,
            fecha_cad=datetime.date(2038, 3, 31)
        )
        relacionVentaPaquete = RelacionVentaPaquete.objects.create(venta=venta, paquete=paquete, cantidad=3, monto=60*3)

    # Comprobar que al cancelar una venta el inventario se actualiza con
    # los paquetes que que esta contenía.
    def test_ac1_actualiza_paquetes_inventario(self):
        self.assertEqual(PaqueteInventario.objects.all()[0].ocupados, 3)
        resp = self.client.get(reverse('ventas:cancelar_venta', kwargs={'id_venta':Venta.objects.all()[0].id}))
        self.assertEqual(PaqueteInventario.objects.all()[0].ocupados, 0)

    # Al cancelar la venta, esta no desaparece de la base de datos.
    def test_ac2_no_borrar_bd(self):
        self.assertEqual(Venta.objects.count(), 1)
        resp = self.client.get(reverse('ventas:cancelar_venta', kwargs={'id_venta':Venta.objects.all()[0].id}))
        self.assertEqual(Venta.objects.count(), 1)

    # Al cancelar la venta, esta no se muestra en la lista de ventas.
    def test_ac3_no_aparece_en_lista(self):
        self.assertEqual(Venta.objects.count(), 1)
        resp = self.client.get(reverse('ventas:ventas'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['ventas'].count(), 1)
        resp = self.client.get(reverse('ventas:cancelar_venta', kwargs={'id_venta':Venta.objects.all()[0].id}))
        self.assertEqual(Venta.objects.count(), 1)
        resp = self.client.get(reverse('ventas:ventas'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['ventas'].count(), 0)
