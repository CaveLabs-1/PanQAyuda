from django.test import TestCase
from ordenes.models import Orden
from recetas.models import  Receta
from django.urls import reverse
import datetime


#US15 - Agregar orden de trabajo
class TestAgregarOrden(TestCase):

    def crear_receta_prueba(self):
        return Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    # Probar que la vista se genera correctamente
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

    # La fecha de enetrega de una orden no puede ser menor a la decha actual.
    def test_fecha_fin_no_menores_a_fecha_fin_actual(self):
        # Simular una petición POST con información valida para crear una nueva orden de trabajo
        # pero con fecha_fin incorrecta.
        receta = self.crear_receta_prueba()
        data = {'receta': receta.id, 'multiplicador' : 2, 'fecha_fin': '1997-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que no se agregó el registro a la base de datos.
        self.assertEqual(Orden.objects.count(), 0)

    # El multiplicador nunca debe ser menor a 0.
    def test_no_aceptar_multiplicadores_menores_a_0(self):

        # Simular una petición POST con un multiplicador negativo.
        receta = self.crear_receta_prueba()
        data = {'receta': receta.id, 'multiplicador' : -2, 'fecha_fin': '2048-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que no se agregó a la base de datos.
        self.assertEqual(Orden.objects.count(), 0)

# Probar que es posible marcar una orden de trabajo como terminada. En caso de que así sea, esta no debe
# aparecer en la lista de ordnes por trabajar.
class TestMarcarOrdenComoTerminada(TestCase):

    # Crear orden de trabajo para realizar pruebas.
    def crear_orden_de_trabajo(slef):
        receta = Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))
        Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-03-20')
        Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-04-20')
        Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-05-20')
        Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-06-20')
        return Orden.objects.count()

    # Comprobar que en la vista sólo se muestran ordenes con status por trabajar.
    def test_render_vista_ordenes_con_status_correcto(self):
        # Crear 4 ordenes de trabajo con status por trabajar.
        registros_ordenes = self.crear_orden_de_trabajo()
        # Obtener datos generados por la view ordenes.
        response = self.client.get(reverse('ordenes:ordenes'))
        # Contar el numero de ordenes que aparecen en la lista de ordenes por trabajar.
        lista_registros = response.context['ordenes'].count()
        # Comprobar que la cantidad de registros con estatus por trabajar y el numero de
        # elementos en la lista de ordenes por trabajar es el mismo.
        self.assertEqual(registros_ordenes, lista_registros)

    def test_cambiar_estatus_de_orden_de_trabajo(self):
        # Crear 4 ordenes de trabajo con status por trabajar.
        registros_ordenes = self.crear_orden_de_trabajo()
        # Recrear petición POST para modificar el estatus de una orden de trabajo
        data = {'id': 2, 'estatus': 2}
        self.client.post(reverse('ordenes:terminar_orden'), data)
        # Comprobar que el registro se modificó correctamente
        self.assertEqual(Orden.objects.get(pk=2).estatus, '2')

    def test_quitar_de_lista_las_ordenes_terminadas(self):
        # Crear 4 ordenes de trabajo con status por trabajar.
        registros_ordenes = self.crear_orden_de_trabajo()
        # Obtener datos generados por la view ordenes.
        response = self.client.get(reverse('ordenes:ordenes'))
        # Contar el numero de ordenes que aparecen en la lista de ordenes por trabajar.
        lista_registros = response.context['ordenes'].count()
        # Comprobar que la cantidad de registros con estatus por trabajar y el numero de
        # elementos en la lista de ordenes por trabajar es el mismo.
        self.assertEqual(registros_ordenes, lista_registros)
        # Recrear petición POST para modificar el estatus de una orden de trabajo
        # Se modificará el registro con id 6
        data = {'id': 6, 'estatus': 2}
        self.client.post(reverse('ordenes:terminar_orden'), data)
        # Comprobar que no aparece en la lista de ordenes por trabajar.
        response = self.client.get(reverse('ordenes:ordenes'))
        # Contar el numero de ordenes que aparecen en la lista de ordenes por trabajar.
        lista_registros = response.context['ordenes'].count()
        # Comprobar que la cantidad de registros con estatus por trabajar -1 (por el que acabamos de quitar) y el numero de
        # elementos en la lista de ordenes por trabajar es el mismo menos.
        self.assertEqual(registros_ordenes-1, lista_registros)
