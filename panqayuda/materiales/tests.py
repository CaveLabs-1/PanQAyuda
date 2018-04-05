from django.test import TestCase
from django.urls import reverse
from materiales.models import Material
from materiales.models import Unidad
from materiales.models import MaterialInventario
from compras.models import Compra
from django.utils import timezone
from django.contrib.auth.models import User

#test agregar materia prima US 11
class TestListaMaterialCatalogo(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary')

    #existe la vista
    def test_valid_session(self):
        session = self.client.session

    def test_ac1_existe_la_vista_html(self):
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(len(resp.context['materiales']),0)
        self.assertEqual(resp.status_code, 200)

    def test_ac2_existe_la_vista_con_algo(self):
        Material.objects.create(nombre="Testerino", codigo=123456789)
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(len(resp.context['materiales']),1)
        self.assertEqual(resp.status_code, 200)

    def test_ac3_la_tabla_no_imprime_objetos_con_estatus_no_disponible(self):
        Material.objects.create(nombre="Test ac3", codigo=123456789, status=0)
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(len(resp.context['materiales']),0)
        self.assertEqual(resp.status_code, 200)
    #se agrega exitosamente el material
    def test_ac4_se_agrega_material_y_se_muestra_en_la_tabla(self):
        self.assertEqual(Material.objects.count(), 0)
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(len(resp.context['materiales']),0)
        self.assertEqual(resp.status_code, 200)
        Material.objects.create(nombre="Test ac4", codigo=123456789)
        resp2 = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(len(resp2.context['materiales']),1)
        self.assertEqual(resp2.status_code, 200)
        Material.objects.create(nombre="Test ac4.2", codigo=123456789)
        resp3 = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(len(resp3.context['materiales']),2)

class TestAgregarMateriaCatalogo(TestCase):

    def setUp(self):
        usuario = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        usuario.save()

    def test_ac1_existe_vista_agregar(self):
        #self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_se_agrega_el_material(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac2", 'codigo':123456789}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 1)

    def test_ac3_no_permite_agregar_material_sin_nombre(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'codigo':123456789}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac4_no_permite_material_sin_codigo(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac 4"}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac5_no_excede_10_caracteres_codigo(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac5", 'codigo':12345678910}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac6_no_excede_100_caracteres_nombre(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac6 excede el limite de 100 caracteres y no permite que se guarde el nomrbe y no se guarda en la base de datos", 'codigo':123456789}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac7_codigo_no_alfa_numerico(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac7", 'codigo':"12d4s6Q890"}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

#Casos de uso US54
class TestListaUnidades(TestCase):

    def test_ac1_existe_la_vista_lista(self):
        resp = self.client.get(reverse('materiales:lista_unidades'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_se_muestra_la_lista_con_unidades_agregadas(sself):
        self.assertEqual(Unidad.objects.count(), 0)
        Unidad.objects.create(nombre="ac2")
        self.assertEqual(Unidad.objects.count(), 1)
        resp = self.client.get(reverse('materiales:lista_unidades'))
        self.assertEqual(len(resp.context['unidades']), 1)

    def test_ac3_existe_vista_agregar(self):
        data = {'nombre':"ac3"}
        resp = self.client.post(reverse('materiales:lista_unidades'), data)
        self.assertEqual(resp.status_code, 200)

    def test_ac4_se_agrega_la_unidad(self):
        self.assertEqual(Unidad.objects.count(), 0)
        data = {'nombre':"ac4"}
        self.client.post(reverse('materiales:lista_unidades'), data)
        self.assertEqual(Unidad.objects.count(), 1)

    def test_ac4_se_agrega_la_unidad(self):
        self.assertEqual(Unidad.objects.count(), 0)
        data = {'nombre':""}
        self.client.post(reverse('materiales:lista_unidades'), data)
        self.assertEqual(Unidad.objects.count(), 0)

# Create your tests here.
