from django.test import TestCase
from django.urls import reverse
from materiales.models import Material
from materiales.models import Unidad
from materiales.models import MaterialInventario
from compras.models import Compra
from django.utils import timezone

#test agregar materia prima
class TestListaMaterialCatalogo(TestCase):
    #existe la vista
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

# class TestAgregarMateriaCatalogo(TestCase):
#
#     def test_ac1_existe_vista_agregar(self):



# Create your tests here.
