from django.test import TestCase
from ordenes.models import Orden
from recetas.models import Receta, RelacionRecetaMaterial, RecetaInventario
from materiales.models import Material, Unidad, MaterialInventario
from compras.models import Compra
from proveedores.models import Proveedor
from django.urls import reverse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group

#US15 - Agregar orden de trabajo
class TestAgregarOrden(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
    #Revisar que la sesión exista
    # def test_valid_session(self):
    #     session = self.client.session

    def datos_prueba(self):
        # Crear registro de unidades de prueba
        midiclorians = Unidad.objects.create(nombre = 'midiclorians')
        lesters = Unidad.objects.create(nombre = 'lesters')
        wruandes = Unidad.objects.create(nombre = 'wruandes')

        # Crear registro de catalogo materiales para pruebas
        azucar = Material.objects.create(nombre = 'Azúcar', codigo = '234', unidad_entrada = lesters, unidad_maestra = lesters, equivale_entrada = 1, equivale_maestra = 1)
        flores = Material.objects.create(nombre = 'Flores', codigo = '420', unidad_entrada = lesters, unidad_maestra = lesters, equivale_entrada = 1, equivale_maestra = 1)
        muchos_colores = Material.objects.create(nombre = 'Muchos Colores', codigo = '4453', unidad_entrada = wruandes, unidad_maestra = wruandes, equivale_entrada = 1, equivale_maestra = 1)
        sustancia_x = Material.objects.create(nombre = 'Sustancia X', codigo = '355', unidad_entrada = midiclorians, unidad_maestra = midiclorians, equivale_entrada = 1, equivale_maestra = 1)

        #Se crea un proveedor par ahacer una compra
        proveedor = Proveedor.objects.create(nombre='Toño', telefono=4423214567, direccion='aqui mero', rfc='hsggw872652', razon_social='SAMS', email='a@j.com')

        #Se ctea una orden de compra para llevar inventario
        compra = Compra.objects.create(proveedor=proveedor, fecha_compra='2038-03-31')

        # Generar registros en el inventario para pruebas
        fecha = timezone.now() + timezone.timedelta(days=3650)
        MaterialInventario.objects.create(material = azucar, compra=compra, unidad_entrada = lesters, cantidad = 1000, costo_unitario = 1, porciones = 1000, porciones_disponible = 1000, fecha_cad = fecha)
        MaterialInventario.objects.create(material = flores, compra=compra, unidad_entrada = lesters, cantidad = 200, costo_unitario = 1, porciones = 200, porciones_disponible = 200, fecha_cad = fecha)
        MaterialInventario.objects.create(material = muchos_colores, compra=compra, unidad_entrada = wruandes, cantidad = 150, costo_unitario = 1, porciones = 150, porciones_disponible = 150, fecha_cad = fecha)
        MaterialInventario.objects.create(material = sustancia_x, compra=compra, unidad_entrada = midiclorians, cantidad = 10, costo_unitario = 1, porciones = 10, porciones_disponible = 10, fecha_cad = fecha)

        # Crear receta de prueba para la alta de ordenes de trabajo
        chicas_sp = Receta.objects.create(nombre = 'Chicas Superpoderosas', cantidad = 3, duration = datetime.timedelta(days=3350))

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
        # Comprobar que la tabla orden inicia sin registros.
        self.assertEqual(Orden.objects.count(), 0)

        # Generar datos de prueba.
        receta = self.datos_prueba()

        # Simular una petición POST con información correcta para crear una nueva orden de trabajo.
        data = {'receta': receta.id, 'multiplicador' : 1, 'fecha_fin': '2038-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que se agregó un registro de una nueva orden de trabajo.
        self.assertEqual(Orden.objects.count(), 1)

        # Verificar que se muestra la nueva orden en la lista de ordenes de trbajo.
        response = self.client.get(reverse('ordenes:ordenes'))
        self.assertEqual(len(response.context['ordenes']), 1)
        self.assertEqual(response.context['ordenes'][0].receta.nombre, "Chicas Superpoderosas")
        self.assertEqual(response.context['ordenes'][0].multiplicador, 1)
        self.assertEqual(response.context['ordenes'][0].fecha_fin, datetime.date(2038, 3, 31))

    # Comprobar que al generar una orden de trabajo se descuenta la cantidad de material registrada en la receta.
    def test_descontar_de_inventario_al_generar_orden(self):
        #Comprobar que la tabla de ordenes inicia sin registros.
        self.assertEqual(Orden.objects.count(), 0)

        # Generar datos de pruebaself.
        receta = self.datos_prueba()

        # Cantidad por material en inventario
        azucar = Material.objects.get(codigo = '234').obtener_cantidad_inventario()
        flores = Material.objects.get(codigo = '420').obtener_cantidad_inventario()
        muchos_colores = Material.objects.get(codigo = '4453').obtener_cantidad_inventario()
        sustancia_x = Material.objects.get(codigo = '355').obtener_cantidad_inventario()


        # Simular una petición POST con información correcta para crear una nueva orden de trabajo.
        data = {'receta': receta.id, 'multiplicador' : 1, 'fecha_fin': '2038-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        #Verificar que se agregó un registro de una nueva orden de trabajo.
        self.assertEqual(Orden.objects.count(), 1)

        # Comprobar que se descontó la cantidad correcta del inventario.
        self.assertEqual(Material.objects.get(codigo = '234').obtener_cantidad_inventario(), azucar-70)
        self.assertEqual(Material.objects.get(codigo = '420').obtener_cantidad_inventario(), flores-120)
        self.assertEqual(Material.objects.get(codigo = '4453').obtener_cantidad_inventario(), muchos_colores-110)
        self.assertEqual(Material.objects.get(codigo = '355').obtener_cantidad_inventario(), sustancia_x-10)

    # En caso de que no haya suficiente material en el inventario para generar la orden, esta no se creará.
    def test_no_se_agrega_si_no_existe_material_inventario(self):
        #Comprobar que la tabla de ordenes inicia sin registros.
        self.assertEqual(Orden.objects.count(), 0)

        # Generar datos de pruebaself.
        receta = self.datos_prueba()

        # Cantidad por material en inventario
        azucar = Material.objects.get(codigo = '234').obtener_cantidad_inventario()
        flores = Material.objects.get(codigo = '420').obtener_cantidad_inventario()
        muchos_colores = Material.objects.get(codigo = '4453').obtener_cantidad_inventario()
        sustancia_x = Material.objects.get(codigo = '355').obtener_cantidad_inventario()


        # Simular una petición POST con información correcta para crear una nueva orden de trabajo.
        # El multiplicador genera una petición que necesita más material del que hay en el inventario.
        data = {'receta': receta.id, 'multiplicador' : 2, 'fecha_fin': '2038-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        #Verificar que no se agregó un registro de una nueva orden de trabajo.
        self.assertEqual(Orden.objects.count(), 0)



    # La fecha de enetrega de una orden no puede ser menor a la fecha actual.
    def test_fecha_fin_no_menores_a_fecha_fin_actual(self):
        # Simular una petición POST con información valida para crear una nueva orden de trabajo
        # pero con fecha_fin incorrecta.
        receta = self.datos_prueba()
        data = {'receta': receta.id, 'multiplicador' : 2, 'fecha_fin': '1997-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que no se agregó el registro a la base de datos.
        self.assertEqual(Orden.objects.count(), 0)

    # El multiplicador nunca debe ser menor a 0.
    def test_no_aceptar_multiplicadores_menores_a_0(self):

        # Simular una petición POST con un multiplicador negativo.
        receta = self.datos_prueba()
        data = {'receta': receta.id, 'multiplicador' : -2, 'fecha_fin': '2048-03-31'}
        self.client.post(reverse('ordenes:ordenes'), data)

        # Verificar que no se agregó a la base de datos.
        self.assertEqual(Orden.objects.count(), 0)

# Probar que es posible marcar una orden de trabajo como terminada. En caso de que así sea, esta no debe
# aparecer en la lista de ordnes por trabajar.
class TestMarcarOrdenComoTerminada(TestCase):
    def datos_prueba(self):
        # Crear registro de unidades de prueba
        midiclorians = Unidad.objects.create(nombre = 'midiclorians')
        lesters = Unidad.objects.create(nombre = 'lesters')
        wruandes = Unidad.objects.create(nombre = 'wruandes')

        # Crear registro de catalogo materiales para pruebas
        azucar = Material.objects.create(nombre = 'Azúcar', codigo = '234', unidad_entrada = lesters, unidad_maestra = lesters, equivale_entrada = 1, equivale_maestra = 1)
        flores = Material.objects.create(nombre = 'Flores', codigo = '420', unidad_entrada = lesters, unidad_maestra = lesters, equivale_entrada = 1, equivale_maestra = 1)
        muchos_colores = Material.objects.create(nombre = 'Muchos Colores', codigo = '4453', unidad_entrada = wruandes, unidad_maestra = wruandes, equivale_entrada = 1, equivale_maestra = 1)
        sustancia_x = Material.objects.create(nombre = 'Sustancia X', codigo = '355', unidad_entrada = midiclorians, unidad_maestra = midiclorians, equivale_entrada = 1, equivale_maestra = 1)

        #Se crea un proveedor par ahacer una compra
        proveedor = Proveedor.objects.create(nombre='Toño', telefono=4423214567, direccion='aqui mero', rfc='hsggw872652', razon_social='SAMS', email='a@j.com')

        #Se ctea una orden de compra para llevar inventario
        compra = Compra.objects.create(proveedor=proveedor, fecha_compra='2038-03-31')

        # Generar registros en el inventario para pruebas
        fecha = timezone.now() + timezone.timedelta(days=3650)
        MaterialInventario.objects.create(material = azucar, compra=compra, unidad_entrada = lesters, cantidad = 1000, costo_unitario = 1, porciones = 1000, porciones_disponible = 1000, fecha_cad = fecha)
        MaterialInventario.objects.create(material = flores, compra=compra, unidad_entrada = lesters, cantidad = 200, costo_unitario = 1, porciones = 200, porciones_disponible = 200, fecha_cad = fecha)
        MaterialInventario.objects.create(material = muchos_colores, compra=compra, unidad_entrada = wruandes, cantidad = 150, costo_unitario = 1, porciones = 150, porciones_disponible = 150, fecha_cad = fecha)
        MaterialInventario.objects.create(material = sustancia_x, compra=compra, unidad_entrada = midiclorians, cantidad = 10, costo_unitario = 1, porciones = 10, porciones_disponible = 10, fecha_cad = fecha)

        # Crear receta de prueba para la alta de ordenes de trabajo
        chicas_sp = Receta.objects.create(nombre = 'Chicas Superpoderosas', cantidad = 3, duration = datetime.timedelta(days=3350))

        # Crear registro de materiales por receta
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = azucar, cantidad = 70)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = flores, cantidad = 120)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = muchos_colores, cantidad = 110)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = sustancia_x, cantidad = 10)

        return chicas_sp

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
    # Crear orden de trabajo para realizar pruebas.
    def crear_orden_de_trabajo(self):

        receta = self.datos_prueba()

        Orden.objects.create(receta = receta, multiplicador = 1, fecha_fin ='2048-03-20')
        Orden.objects.create(receta = receta, multiplicador = 1, fecha_fin ='2048-04-20')
        Orden.objects.create(receta = receta, multiplicador = 1, fecha_fin ='2048-05-20')
        Orden.objects.create(receta = receta, multiplicador = 1, fecha_fin ='2048-06-20')
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
        orden = Orden.objects.first()
        data = {'id': orden.id, 'estatus': 2}
        self.client.post(reverse('ordenes:terminar_orden'), data)
        # Comprobar que el registro se modificó correctamente
        self.assertEqual(Orden.objects.get(id=orden.id).estatus, '2')

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
        data = {'id': 9, 'estatus': 2}
        self.client.post(reverse('ordenes:terminar_orden'), data)
        # Comprobar que no aparece en la lista de ordenes por trabajar.
        response = self.client.get(reverse('ordenes:ordenes'))
        # Contar el numero de ordenes que aparecen en la lista de ordenes por trabajar.
        lista_registros = response.context['ordenes'].count()
        # Comprobar que la cantidad de registros con estatus por trabajar -1 (por el que acabamos de quitar) y el numero de
        # elementos en la lista de ordenes por trabajar es el mismo menos.
        self.assertEqual(registros_ordenes-1, lista_registros)


class TestCancelarOrden(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    def datos_prueba(self):
        # Crear registro de unidades de prueba
        midiclorians = Unidad.objects.create(nombre = 'midiclorians')
        lesters = Unidad.objects.create(nombre = 'lesters')
        wruandes = Unidad.objects.create(nombre = 'wruandes')

        # Crear registro de catalogo materiales para pruebas
        azucar = Material.objects.create(nombre = 'Azúcar', codigo = '234', unidad_entrada = lesters, unidad_maestra = lesters, equivale_entrada = 1, equivale_maestra = 1)
        flores = Material.objects.create(nombre = 'Flores', codigo = '420', unidad_entrada = lesters, unidad_maestra = lesters, equivale_entrada = 1, equivale_maestra = 1)
        muchos_colores = Material.objects.create(nombre = 'Muchos Colores', codigo = '4453', unidad_entrada = wruandes, unidad_maestra = wruandes, equivale_entrada = 1, equivale_maestra = 1)
        sustancia_x = Material.objects.create(nombre = 'Sustancia X', codigo = '355', unidad_entrada = midiclorians, unidad_maestra = midiclorians, equivale_entrada = 1, equivale_maestra = 1)

        #Se crea un proveedor par ahacer una compra
        proveedor = Proveedor.objects.create(nombre='Toño', telefono=4423214567, direccion='aqui mero', rfc='hsggw872652', razon_social='SAMS', email='a@j.com')

        #Se ctea una orden de compra para llevar inventario
        compra = Compra.objects.create(proveedor=proveedor, fecha_compra='2038-03-31')

        # Generar registros en el inventario para pruebas
        fecha = timezone.now() + timezone.timedelta(days=3650)
        MaterialInventario.objects.create(material = azucar, compra=compra, unidad_entrada = lesters, cantidad = 1000, costo_unitario = 1, porciones = 1000, porciones_disponible = 1000, fecha_cad = fecha)
        MaterialInventario.objects.create(material = flores, compra=compra, unidad_entrada = lesters, cantidad = 200, costo_unitario = 1, porciones = 200, porciones_disponible = 200, fecha_cad = fecha)
        MaterialInventario.objects.create(material = muchos_colores, compra=compra, unidad_entrada = wruandes, cantidad = 150, costo_unitario = 1, porciones = 150, porciones_disponible = 150, fecha_cad = fecha)
        MaterialInventario.objects.create(material = sustancia_x, compra=compra, unidad_entrada = midiclorians, cantidad = 10, costo_unitario = 1, porciones = 10, porciones_disponible = 10, fecha_cad = fecha)

        # Crear receta de prueba para la alta de ordenes de trabajo
        chicas_sp = Receta.objects.create(nombre = 'Chicas Superpoderosas', cantidad = 3, duration = datetime.timedelta(days=3350))

        # Crear registro de materiales por receta
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = azucar, cantidad = 70)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = flores, cantidad = 120)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = muchos_colores, cantidad = 110)
        RelacionRecetaMaterial.objects.create(receta = chicas_sp, material = sustancia_x, cantidad = 10)

        return chicas_sp

    # Crear orden de trabajo para realizar pruebas.
    def crear_orden_de_trabajo(self):

        receta = self.datos_prueba()
        orden = Orden.objects.create(receta = receta, multiplicador = 1, fecha_fin ='2048-06-20')
        return orden.id


    # Comprobar que se ha cambiado el status de la orden de trabajo
    def test_estatus_0(self):
        r = self.crear_orden_de_trabajo()
        self.assertEqual(Orden.objects.count(), 1)
        data = {'id':r, 'estatus':0}
        self.client.post(reverse('ordenes:cancelar_orden'), data)
        resp = self.client.get(reverse('ordenes:cancelar_orden'))
        self.assertEqual(len(resp.context['ordenes']), 0)
