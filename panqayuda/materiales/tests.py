from django.test import TestCase
from django.urls import reverse
from materiales.models import Material

#test agregar materia prima
class TestAgregarMaterial(TestCase):
    #existe la vista
    def test_existe_la_vista(self):
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(resp.status_code, 200)

    #se agrega exitosamente el material
    # def test_ac1_se_agrega_material(self):
    #     self.assertEqual(Material.objects.count(), 0)
    #     data = {'nombre':"Pan", 'unidad':""}
# Create your tests here.
