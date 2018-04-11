from django.test import TestCase
from django.urls import reverse
from compras.models import Compra
from compras.models import RelacionCompraMaterial
import datetime
from django.contrib.auth.models import User, Group
from django.utils import timezone
from proveedores.models import Proveedor
from materiales.models import Material, Unidad, MaterialInventario
#test US 10
class TestListaCompras(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        proveedor = Proveedor.objects.create(
            nombre="TestLista",
            telefono=4151043944,
            direccion="Aqui mero patatero",
            rfc="12342121",
            razon_social="Un tipazo",
            email="test@ejemplo.com"
        )
        compra = Compra.objects.create(proveedor=proveedor, fecha_compra="2059-03-03 12:31:06-05")
        material = Material.objects.create(nombre="Material Test", codigo=12344)
        unidad = Unidad.objects.create(nombre="Unidad")
        materialinv = MaterialInventario.objects.create(
            material=material,
            unidad_entrada=unidad,
            cantidad=12,
            cantidad_salida=12,
            costo=100,
            fecha_cad="2059-03-03 12:31:06-05"
        )
        RelacionCompraMaterial.objects.create(
            compra=compra,
            material=materialinv,
            cantidad=1
        )

    def test_ac1_Existe_la_vista_de_listado(self):
        resp = self.client.get(reverse('compras:compras'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_Muestra_las_compras_correctas(self):
        self.assertEqual(Compra.objects.count(), 1)
        resp = self.client.get(reverse('compras:compras'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['compras'].count(), 1)
        #self.assertEqual(resp.context['compras'].proveedor, "TestLista")

    def test_ac3_La_vista_detalle_existe(self):
        self.assertEqual(Compra.objects.count(), 1)
        id = Compra.objects.first()
        data = {'id_compra':id.pk}
        resp = self.client.post(reverse('compras:lista_detalle_compra'), data)
        self.assertEqual(resp.status_code, 200)

    def test_ac4_lista_detalle_es_correcta(self):
        self.assertEqual(Compra.objects.count(), 1)
        id = Compra.objects.first()
        data = {'id_compra':id.pk}
        resp = self.client.post(reverse('compras:lista_detalle_compra'), data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['compra'].proveedor, id.proveedor)
# Create your tests here.
