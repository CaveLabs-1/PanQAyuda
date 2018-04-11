from django.test import TestCase
from ordenes.models import Orden
from recetas.models import Receta, RelacionRecetaMaterial, RecetaInventario
from materiales.models import Material, Unidad, MaterialInventario
from django.urls import reverse
from django.utils import timezone
import datetime


#US15 - Agregar orden de trabajo
class TestAgregarOrden(TestCase):

    #Revisar que la sesión exista
    # def test_valid_session(self):
    #     session = self.client.session

    def datos_prueba(self):
        # Crear registro de unidades de prueba
        midiclorians = Unidad.objects.create(nombre = 'midiclorians')
        lesters = Unidad.objects.create(nombre = 'lesters')
        wruandes = Unidad.objects.create(nombre = 'wruandes')

        # Crear registro de catalogo materiales para pruebas
        azucar = Material.objects.create(nombre = 'Azúcar', codigo = '234')
        flores = Material.objects.create(nombre = 'Flores', codigo = '420')
        muchos_colores = Material.objects.create(nombre = 'Muchos Colores', codigo = '4453')
        sustancia_x = Material.objects.create(nombre = 'Sustancia X', codigo = '355')

        # Generar registros en el inventario para pruebas
        MaterialInventario.objects.create(material = azucar, unidad_entrada = lesters, cantidad = 1000, cantidad_salida = 100, cantidad_disponible = 100, costo = 20.50)
        MaterialInventario.objects.create(material = flores, unidad_entrada = lesters, cantidad = 50, cantidad_salida = 200, cantidad_disponible = 200, costo = 85.70)
        MaterialInventario.objects.create(material = muchos_colores, unidad_entrada = wruandes, cantidad = 350, cantidad_salida = 150, cantidad_disponible = 150, costo = 73.50)
        MaterialInventario.objects.create(material = sustancia_x, unidad_entrada = midiclorians, cantidad = 30, cantidad_salida = 10, cantidad_disponible = 10, costo = 27000.50)

        # Crear receta de prueba para la alta de ordenes de trabajo
        chicas_sp = Receta.objects.create(nombre = 'Chicas Superpoderosas', cantidad = 3, duration = datetime.timedelta(days=3350))

        print(azucar.obtener_cantidad_inventario())
        print('********')

        # Crear registro de materiales por receta
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = azucar, cantidad = 70)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = flores, cantidad = 120)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = muchos_colores, cantidad = 110)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = sustancia_x, cantidad = 10)

        return chicas_sp

    # Probar que la vista se genera correctamente
    def test_render_vista_ordenes(self):
        response = self.client.get(reverse('ordenes:ordenes'))
        self.assertEqual(response.status_code, 200)

    # Comprobar que es posible agregar una orden de trabajo a la lista de ordenes de tra
    def test_agregar_orden_a_vista_de_ordenes(self):
        # # Comprobar que la tabla orden inicia sin registros.
        # self.assertEqual(Orden.objects.count(), 0)
        #
        # # Simular una petición POST con información correcta para crear una nueva orden de trabajo.
        receta = self.datos_prueba()
        #
        # data = {'receta': receta.id, 'multiplicador' : 2, 'fecha_fin': '2038-03-31'}
        # self.client.post(reverse('ordenes:ordenes'), data)
        #
        # # Verificar que se agregó un registro de una nueva orden de trabajo.
        # self.assertEqual(Orden.objects.count(), 1)
        #
        # # Verificar que se muestra la nueva orden en la lista de ordenes de trbajo.
        # response = self.client.get(reverse('ordenes:ordenes'))
        # self.assertEqual(len(response.context['ordenes']), 1)
        # self.assertEqual(response.context['ordenes'][0].receta.nombre, "Receta de prueba")
        # self.assertEqual(response.context['ordenes'][0].multiplicador, 2)
        # self.assertEqual(response.context['ordenes'][0].fecha_fin, datetime.date(2038, 3, 31))

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

# # Probar que es posible marcar una orden de trabajo como terminada. En caso de que así sea, esta no debe
# # aparecer en la lista de ordnes por trabajar.
# class TestMarcarOrdenComoTerminada(TestCase):
#
#     # Crear orden de trabajo para realizar pruebas.
#     def crear_orden_de_trabajo(slef):
#         receta = Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))
#         Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-03-20')
#         Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-04-20')
#         Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-05-20')
#         Orden.objects.create(receta = receta, multiplicador = 2, fecha_fin ='2048-06-20')
#         return Orden.objects.count()
#
#     # Comprobar que en la vista sólo se muestran ordenes con status por trabajar.
#     def test_render_vista_ordenes_con_status_correcto(self):
#         # Crear 4 ordenes de trabajo con status por trabajar.
#         registros_ordenes = self.crear_orden_de_trabajo()
#         # Obtener datos generados por la view ordenes.
#         response = self.client.get(reverse('ordenes:ordenes'))
#         # Contar el numero de ordenes que aparecen en la lista de ordenes por trabajar.
#         lista_registros = response.context['ordenes'].count()
#         # Comprobar que la cantidad de registros con estatus por trabajar y el numero de
#         # elementos en la lista de ordenes por trabajar es el mismo.
#         self.assertEqual(registros_ordenes, lista_registros)
#
#     def test_cambiar_estatus_de_orden_de_trabajo(self):
#         # Crear 4 ordenes de trabajo con status por trabajar.
#         registros_ordenes = self.crear_orden_de_trabajo()
#         # Recrear petición POST para modificar el estatus de una orden de trabajo
#         data = {'id': 2, 'estatus': 2}
#         self.client.post(reverse('ordenes:terminar_orden'), data)
#         # Comprobar que el registro se modificó correctamente
#         self.assertEqual(Orden.objects.get(pk=2).estatus, '2')
#
#     def test_quitar_de_lista_las_ordenes_terminadas(self):
#         # Crear 4 ordenes de trabajo con status por trabajar.
#         registros_ordenes = self.crear_orden_de_trabajo()
#         # Obtener datos generados por la view ordenes.
#         response = self.client.get(reverse('ordenes:ordenes'))
#         # Contar el numero de ordenes que aparecen en la lista de ordenes por trabajar.
#         lista_registros = response.context['ordenes'].count()
#         # Comprobar que la cantidad de registros con estatus por trabajar y el numero de
#         # elementos en la lista de ordenes por trabajar es el mismo.
#         self.assertEqual(registros_ordenes, lista_registros)
#         # Recrear petición POST para modificar el estatus de una orden de trabajo
#         # Se modificará el registro con id 6
#         data = {'id': 6, 'estatus': 2}
#         self.client.post(reverse('ordenes:terminar_orden'), data)
#         # Comprobar que no aparece en la lista de ordenes por trabajar.
#         response = self.client.get(reverse('ordenes:ordenes'))
#         # Contar el numero de ordenes que aparecen en la lista de ordenes por trabajar.
#         lista_registros = response.context['ordenes'].count()
#         # Comprobar que la cantidad de registros con estatus por trabajar -1 (por el que acabamos de quitar) y el numero de
#         # elementos en la lista de ordenes por trabajar es el mismo menos.
#         self.assertEqual(registros_ordenes-1, lista_registros)
#
#
# class TestCancelarOrden(TestCase):
#
#     def crear_receta(self):
#         return Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))
#
#
#     def crear_orden(self):
#         return Orden.objects.create(multiplicador=1, estatus=1, receta=self.crear_receta())
#
#
#     def test_estatus_0(self):
#         r = self.crear_orden()
#         self.assertEqual(Orden.objects.count(), 1)
#         data = {'id':r.id, 'estatus':0}
#         self.client.post(reverse('ordenes:cancelar_orden'), data)
#         resp = self.client.get(reverse('ordenes:cancelar_orden'))
#         self.assertEqual(len(resp.context['ordenes']), 0)
