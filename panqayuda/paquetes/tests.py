from django.test import TestCase
from paquetes.models import Paquete
from django.urls import reverse
# Create your tests here.

class TestBorrarPaqueteCatalogo(TestCase):

    def crear_paquete(self):
        return Paquete.objects.create(nombre="Paquete de Prueba", precio=12.0)

    def test_ac_26_1(self):
        self.assertEqual(Paquete.objects.count(), 0)
        p = self.crear_paquete()
        # data = {'nombre': "Paquete de Prueba", 'precio': 12}
        # self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 1)

        # self.client.post(reverse('paquetes:borrar_paquete'), p.id)
        self.client.get(reverse('paquetes:borrar_paquete', kwargs={'id_paquete':p.id}))
        self.assertEqual(Paquete.objects.count(), 1)


    def test_ac_26_2(self):
        p = self.crear_paquete()
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(len(resp.context['paquetes']),1)
        self.client.get(reverse('paquetes:borrar_paquete', kwargs={'id_paquete':p.id}))
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(len(resp.context['paquetes']),0)


    def test_ac_26_3(self):
        p = self.crear_paquete()
        self.client.get(reverse('paquetes:borrar_paquete', kwargs={'id_paquete':p.id}))
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(Paquete.objects.filter(deleted_at__isnull=True).count(), 0)
