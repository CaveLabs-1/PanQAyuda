from django.test import TestCase
from paquetes.models import Paquete
# Create your tests here.

class TestBorrarPaqueteCatalogo(TestCase):

    def crear_paquete(self):
        return Paquete.objects.create(nombre="Paquete de Prueba", precio=12.0)

    def test_borrado(self):
        self.assertEqual(Paquete.objects.count(), 0)

        data = {'nombre': "Paquete de Prueba", 'precio': 12}
        self.client.post(reverse('paquetes:agregar_paquete'), data)

        self.assertEqual(Paquete.objects.count(), 1)

        self.client.post(reverse('paquetes:borrar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 0)
