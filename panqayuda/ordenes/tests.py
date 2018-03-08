from django.test import TestCase
from ordenes.models import Orden
from recetas.models import  Receta
from django.urls import reverse
import datetime


#US15 - Agregar orden de trabajo
class TestAgregarOrden(TestCase):

    def crear_receta_prueba(self):
        return Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    def test_render_vista_ordenes(self):
        response = self.client.get(reverse('ordenes:ordenes'))
        self.assertEqual(response.status_code, 200)

    # Comprobar que es posible agregar una orden de trabajo a la lista de ordenes de tra
    def test_agregar_orden_a_vista_de_ordenes(self):
        # Comprobar que la tabla orden inicia sin registros.
        self.assertEqual(Orden.objects.count(), 0)

        # Simular una petición POST con información correcta para crear una nueva orden de trabajo.
        receta = self.crear_receta_prueba()

        data = {'receta': receta.id, 'multiplicador' : 2, 'fecha_fin': '2038-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que se agregó un registro de una nueva orden de trabajo.
        self.assertEqual(Orden.objects.count(), 1)

        # Verificar que se muestra la nueva orden en la lista de ordenes de trbajo.
        response = self.client.get(reverse('ordenes:ordenes'))
        self.assertEqual(len(response.context['ordenes']), 1)
        self.assertEqual(response.context['ordenes'][0].receta.nombre, "Receta de prueba")
        self.assertEqual(response.context['ordenes'][0].multiplicador, 2)
        self.assertEqual(response.context['ordenes'][0].fecha_fin, datetime.date(2038, 3, 31))


    def test_fecha_fin_no_menores_a_fecha_fin_actual(self):
        # Simular una petición POST con información valida para crear una nueva orden de trabajo
        # pero con fecha_fin incorrecta.
        receta = self.crear_receta_prueba()
        data = {'receta': receta.id, 'multiplicador' : 2, 'fecha_fin': '1997-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que no se agregó el registro a la base de datos.
        self.assertEqual(Orden.objects.count(), 0)

    def test_no_aceptar_multiplicadores_menores_a_0(self):

        # Simular una petición POST con un multiplicador negativo.
        receta = self.crear_receta_prueba()
        data = {'receta': receta.id, 'multiplicador' : -2, 'fecha_fin': '2048-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que no se agregó a la base de datos.
        self.assertEqual(Orden.objects.count(), 0)
