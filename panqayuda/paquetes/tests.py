from django.test import TestCase
from paquetes.models import Paquete, Recetas_por_paquete
from recetas.models import Receta
import datetime
from django.urls import reverse

#Test creado por Manuel
class TestEditarPaqueteCatalogo(TestCase):

    def setUp(self):
        return Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    def crear_Paquete(self):
        return Paquete.object.create(nombre="Paquete de prueba", precio=10, estatus=1)

    def crear_relacion_paquete_receta(self, receta, paquete):
        return Recetas_por_paquete.object.create(paquete=paquete, receta=receta, cantidad=2)

    def test_vista_editar_paquete(self):
        resp = self.client.get(reverse('paquetes:editar_paquete'))
        self.assertEqual(resp.status_code, 200)

    def test_ac_25_1(self):
        #Checar si la base de datos esta vacia de paquetes
        self.assertEqual(Paquete.objects.count(), 0)
        
# Create your tests here.
