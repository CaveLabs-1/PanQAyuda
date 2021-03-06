from django.test import TestCase
from materiales.models import Material, Unidad
from recetas.models import Receta, RelacionRecetaMaterial, RecetaInventario
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User, Group
from materiales.models import MaterialInventario
from compras.models import Compra
from proveedores.models import Proveedor
from materiales.models import Unidad
from ordenes.models import Orden
from django.utils import timezone

#US27-Agregar Receta
class TestAgregarReceta(TestCase):

    #Revisar que la sesión exista
    def setUp(self):
        #Crear usuario de prueba
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()

        #Crear unidades de prueba
        Unidad.objects.create(nombre="kg")
        Unidad.objects.create(nombre="pz")

        self.client.login(username='temporary', password='temporary')

    def crear_receta_prueba(self):
        return Receta.objects.create(nombre="Producto semiterminado de prueba", codigo='2342', cantidad=20, duration=timezone.timedelta(days=1))

    def crear_material_prueba(self):
        unidad_entrada = Unidad.objects.first()
        unidad_maestra = Unidad.objects.last()
        equivale_entrada = 1
        equivale_maestra = 16

        return Material.objects.create(nombre="Huevo", unidad_entrada=unidad_entrada, equivale_entrada=equivale_entrada, unidad_maestra=unidad_maestra,
                                       equivale_maestra=equivale_maestra,codigo="T1")

    def crear_relacion_receta_material(self,receta,material):
        RelacionRecetaMaterial.objects.create(receta=receta, material=material, cantidad=10)


    #Verificar que la vista sea correctamente encontrada
    def test_vista_agregar_receta(self):
        resp = self.client.get(reverse('recetas:agregar_receta'))
        self.assertEqual(resp.status_code,200)

    #AC 27.1, 27.5, 27.7 La receta se puede ver en la lista de recetas una vez que se ha agregado, se agrega aunque
    #no se haya de terminado de agregar materiales, y puede tener cualquier caracter
    def test_ac_27_1(self):
        #Base de datos vacía
        self.assertEqual(Receta.objects.count(), 0)

        #Simular POST con información correcta
        data = {'nombre': "Producto semiterminado de prueba", 'codigo':'2342', 'cantidad': 20, 'duracion_en_dias':'1'}
        self.client.post(reverse('recetas:agregar_receta'), data)

        #Verificar que se creó el objeto
        self.assertEqual(Receta.objects.count(), 1)

        #Verificar la lista de recetas
        resp = self.client.get(reverse('recetas:lista_de_recetas'))
        self.assertEqual(len(resp.context['recetas']), 1)
        self.assertEqual(resp.context['recetas'][0].nombre, "Producto semiterminado de prueba")

        #Crear receta con caracteres especiales
        data = {'nombre': "Canción de náàvïda", 'codigo':'2342', 'cantidad': 20, 'duracion_en_dias': '1'}
        self.client.post(reverse('recetas:agregar_receta'), data)
        self.assertEqual(Receta.objects.count(), 2)

    #AC 27.2 Los materiales que ya están en la receta no aparecen disponibles para agregar
    def test_ac_27_2(self):
        #Crear objetos de prueba
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        #Asignar material a receta
        self.crear_relacion_receta_material(r,m)

        #Verificar que el material no se le muestra al usuario para agregar
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        self.assertEqual(len(resp.context['materiales_disponibles']),0)


    #AC 27.3 La cantidad de producto que genera la receta sólo puede ser un número positivo entero.
    def test_ac_27_3(self):
        #POST con cantidad negativa
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo':'2342', 'cantidad': '-5', 'duracion_en_dias': '1'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)

        #Verificar que no se haya creado
        self.assertEqual(Receta.objects.count(),0)

        #POST con cantidad decimal
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo':'2342', 'cantidad': '0.05', 'duracion_en_dias': '1'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)

        # Verificar que no se haya creado
        self.assertEqual(Receta.objects.count(), 0)

        #POST con cantidad entera positiva
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo': '2342', 'cantidad': '1', 'duracion_en_dias': '1'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)
        self.assertEqual(Receta.objects.count(), 1)

    #AC 27.4 No se puede agregar un material que ya esté en la receta
    def test_ac_27_4(self):
        #Asignar material a receta
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        self.crear_relacion_receta_material(r,m)
        #Verificar que se hizo la asignación
        self.assertEqual(r.material.count(), 1)

        #POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}), data)

        #Verificar que no se haya hecho la asignación
        self.assertEqual(r.material.count(), 1)

        #Verificar mensaje de error
        self.assertFormError(resp, 'form','material', "La materia prima seleccionada ya está en la receta del producto semiterminado.")

    #AC 27.6 No se puede agregar una receta con un nombre existente
    def test_ac_27_6(self):
        #Crear PST de prueba con nombre 'Producto semiterminado de prueba'
        r = self.crear_receta_prueba()
        # POST con nombre repetido
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo': '2342', 'cantidad': '10', 'duracion_en_dias': '1 days'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)

        #Verificar que no se haya creado la receta
        self.assertEqual(Receta.objects.count(),1)

        #Verificar mensaje de error
        self.assertFormError(resp,'form','nombre',"Este producto semiterminado ya existe")

    #AC 27.8 Cuando se agrega un material con su respectiva cantidad a la receta, se agrega en la lista de materiales
    # de la receta
    def test_ac_27_8(self):
        # Asignar material a receta
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()

        # POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        # Verificar que está en la lista de materiales
        self.assertEqual(len(resp.context['materiales_actuales']), 1)
        self.assertEqual(resp.context['materiales_actuales'][0].material.nombre, m.nombre)

    #AC 27.9 Sólo un usuario administrtivo puede agregar una receta -- PENDIENTE

    #AC 27.10 Cuando se termina agregar la receta, el usuario visualiza un resumen de esta.
    def test_ac_27_10(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        #Verificar que el link que lleve a la vista de detalle se encuentre en la respuesta
        self.assertContains(resp, reverse('recetas:detallar_receta', kwargs={'id_receta':r.id}))
        #Verificar que la vista se muestra correctamente
        resp = self.client.get(reverse('recetas:detallar_receta', kwargs={'id_receta':r.id}))
        self.assertEquals(resp.status_code,200)

    #AC 27.11 Un material que se agrega a la receta no puede dejarse sin cantidad o cantidad 0.
    def test_ac_27_11(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        # POST con cantidad negativa
        data = {'material': m.nombre, 'cantidad': '-1', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)

        # POST con cantidad cero
        data = {'material': m.nombre, 'cantidad': '0', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)

        # POST sin cantidad
        data = {'material': 'Huevo', 'cantidad': '', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)
        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)
        # Verificar mensaje de error
        self.assertFormError(resp,'form','cantidad','Debes seleccionar una cantidad.')
        # POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que sí se hizo la relación
        self.assertEqual(r.material.count(), 1)
        self.assertEqual(r.material.first().status, 1)

    #AC 27.12 El nombre de la receta no puede estar vacío
    def ac_27_12(self):
        # Simular POST con información correcta
        data = {'nombre': "", 'codigo': '2342', 'cantidad': 20, 'duracion_en_dias': '1'}
        self.client.post(reverse('recetas:agregar_receta'), data)

        self.assertEqual(Receta.objects.count(),0)

    #AC 27.13 No se pueden agregan materiales a una receta inexistente
    def ac_27_13(self):
        #Verificar que una receta inexistente regrese 404
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_materiales':1750}))
        self.assertEqual(resp.status_code, 404)

        #Verificar que una receta que se haya dado de baja arroje error 404
        r = self.crear_receta_prueba()
        r.status = 0

        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_materiales':1}))
        self.assertEqual(resp.status_code, 404)


#US28-Editar Receta
class TestEditarReceta(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()

        # Crear unidades de prueba
        Unidad.objects.create(nombre="kg")
        Unidad.objects.create(nombre="pz")

        self.client.login(username='temporary', password='temporary')

    def crear_receta_prueba(self):
        return Receta.objects.create(nombre="Producto semiterminado de prueba", codigo='2342', cantidad=20, duration=timezone.timedelta(days=1))

    def crear_material_prueba(self):
        unidad_entrada = Unidad.objects.first()
        unidad_maestra = Unidad.objects.last()
        equivale_entrada = 1
        equivale_maestra = 16

        return Material.objects.create(nombre="Huevo", unidad_entrada=unidad_entrada, equivale_entrada=equivale_entrada,
                                       unidad_maestra=unidad_maestra,
                                       equivale_maestra=equivale_maestra, codigo="T1")

    def crear_relacion_receta_material(self,receta,material):
        RelacionRecetaMaterial.objects.create(receta=receta, material=material, cantidad=10)

    #Verificar que la vista sea correctamente encontrada
    def test_vista_editar_receta(self):
        #Crear objetos de prueba
        r = self.crear_receta_prueba()

        resp = self.client.get(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}))
        self.assertEqual(resp.status_code,200)

    # 28.1 No se puede editar una receta con un nombre existente
    def test_receta_nombre_existente(self):
        # Crear receta de prueba con nombre 'Receta de prueba'
        r = self.crear_receta_prueba()

        #Agregar nuevo producto semiterminado
        data = {'nombre': 'Producto semiterminado 2', 'codigo': '2342', 'cantidad': '10', 'duracion_en_dias': '1'}
        self.client.post(reverse('recetas:agregar_receta'), data)

        r2 = Receta.objects.get(nombre="Producto semiterminado 2")
        #Tratar de editar producto semiterminado recién creado y asignarle el nombre del primero
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo': '2342', 'cantidad': '10', 'duracion_en_dias': '1'}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r2.id}), data)
        # Verificar que no se haya editado la receta
        self.assertEqual(r2.nombre, "Producto semiterminado 2")

        # Verificar mensaje de error
        self.assertFormError(resp, 'form', 'nombre', "Este producto semiterminado ya existe")

    # 28.2 El nombre de la receta no puede estar vacío
    def test_nombre_vacio(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()

        # Simular POST con información correcta
        data = {'nombre': "", 'codigo': '2342', 'cantidad': 20, 'duracion_en_dias': '1'}
        self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        #Verificar que no se editó el producto semiterminado
        self.assertEqual(r.nombre, "Producto semiterminado de prueba")


    #28.3 La cantidad de producto que genera la receta sólo puede ser un número positivo entero.
    def test_cantidad_producto_positiva(self):
        #Crear objetos de prueba
        r = self.crear_receta_prueba()

        #POST con cantidad negativa
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo': '2342', 'cantidad': '-5', 'duracion_en_dias': '1'}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        #Verificar que no se haya editado
        self.assertTrue(r.cantidad is not -5)

        #POST con cantidad decimal
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo': '2342', 'cantidad': '0.05', 'duracion_en_dias': '1'}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        # Verificar que no se haya creado
        self.assertTrue(r.cantidad is not 0.05)

        #POST con cantidad entera positiva
        data = {'nombre': 'Producto semiterminado de prueba', 'codigo': '2342', 'cantidad': '1', 'duracion_en_dias': '1'}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)
        self.assertTrue(r.cantidad,1)

        #28.4 Cuando se edita el producto semiterminado, los cambios son visibles
        def test_cantidad_producto_positiva(self):
            # Crear objetos de prueba
            r = self.crear_receta_prueba()

            # POST con cantidad entera positiva
            data = {'nombre': 'Producto semiterminado', 'codigo': '2342', 'cantidad': '5', 'duracion_en_dias': '10'}
            self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)
            self.assertEqual(r.cantidad, 5)
            self.assertEqual(r.nombre, "Producto semiterminado")

# ------------------------------ US 29 Borrar Receta ------------------------------ #


class TestBorrarReceta(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()

        # Crear unidades de prueba
        Unidad.objects.create(nombre="kg")
        Unidad.objects.create(nombre="pz")

        self.client.login(username='temporary', password='temporary')

    def crear_receta(self):
        return Receta.objects.create(nombre="Prueba de Bolillo", codigo='2342', cantidad=12, duration=timezone.timedelta(days=1))

    #Al borrar sigue existiendo en la base de datos
    def test_ac_29_1(self):
        self.assertEqual(Receta.objects.count(), 0)
        r = self.crear_receta()
        self.assertEqual(Receta.objects.count(), 1)
        self.client.get(reverse('recetas:borrar_receta', kwargs={'id_receta':r.id}))
        self.assertEqual(Receta.objects.count(), 1)

    #Ya no aparece en la lista de productos semiterminados despues de borrar
    def test_ac_29_2(self):
        r = self.crear_receta()
        resp = self.client.get(reverse('recetas:lista_de_recetas'))
        self.assertEqual(len(resp.context['recetas']),1)
        self.client.get(reverse('recetas:borrar_receta', kwargs={'id_receta':r.id}))
        resp = self.client.get(reverse('recetas:lista_de_recetas'))
        self.assertEqual(len(resp.context['recetas']),0)


#Es parte de la US19
class TestListaRecetasInventario(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        #Crear Receta
        Receta.objects.create(nombre="Receta de prueba", duration=timezone.timedelta(days=1))

        #Crear Receta Inventario
        RecetaInventario.objects.create(nombre=Receta.objects.first(), cantidad=10, fecha_cad=timezone.now() + timezone.timedelta(days=10))

        #Crear Receta Inventario con algunos ocupados
        RecetaInventario.objects.create(nombre=Receta.objects.first(), cantidad=10, ocupados=5, fecha_cad=timezone.now() + timezone.timedelta(days=5))

        #Crear Receta Inventario con todos ocupados
        RecetaInventario.objects.create(nombre=Receta.objects.first(), cantidad=10, ocupados=10, fecha_cad=timezone.now() + timezone.timedelta(days=10))

        #Crear Receta Inventario caducada
        RecetaInventario.objects.create(nombre=Receta.objects.first(), cantidad=10, ocupados=0, fecha_cad=timezone.now() + timezone.timedelta(days=1))

        # Crear Receta Inventario eliminada
        RecetaInventario.objects.create(nombre=Receta.objects.first(), cantidad=10, ocupados=0,fecha_cad=timezone.now() + timezone.timedelta(days=1), estatus=0, deleted_at=timezone.now())

        #Crear Receta eliminada
        Receta.objects.create(nombre="Receta de prueba eliminada", codigo='2342', duration=timezone.timedelta(days=1), status=0)

    def test_vista_existente(self):
        resp = self.client.get(reverse('recetas:lista_recetas_inventario'))
        self.assertEqual(resp.status_code,200)

        #Verificar que no se cuentan los que están eliminados u ocupados
        self.assertEqual(resp.context['catalogo_recetas'][0].obtener_cantidad_inventario_con_caducados(), 25)

    def test_detalle_receta_inventario(self):
        data = {'id_receta': Receta.objects.first().id}
        resp = self.client.post(reverse('recetas:detalle_recetas_inventario'),data)

        #Verificar el detalle de la lista de recetas

        #Sólo aparecen las que tienen piezas disponibles ni las eliminadas
        self.assertEqual(resp.context['detalle_recetas_en_inventario'].count(), 3)

        #Se señalan los que están caducados

#Test US 34
class TestVerCostoRecetaInventario(TestCase):

    #Setup AC 34.1
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                        is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        #Agregar Unidades
        data = {'nombre': "kilos"}
        self.client.post(reverse('materiales:lista_unidades'), data)

        data = {'nombre': "pieza"}
        self.client.post(reverse('materiales:lista_unidades'), data)
        # Agregar Proveedor
        data = {
            'nombre': "Nombre Proveedor",
            'telefono': '4424708341',
            'email': 'ale@hot.com',
            'direccion': 'prueba de direccion',
            'rfc': '1231230',
            'razon_social': 'razon social'
        }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        # Agregar Catalogo Materia Prima
        unidad_entrada = Unidad.objects.first()
        unidad_maestra = Unidad.objects.last()
        data={
            'nombre':'Material',
            'codigo':'1223123',
            'equivale_entrada':'1',
            'unidad_entrada':unidad_entrada.id,
            'equivale_maestra':'1',
            'unidad_maestra':unidad_maestra.id
        }
        self.client.post(reverse('materiales:materiales'), data)
        Proveedor.objects.create(
            nombre='Proveedor',
            telefono='4424708341',
            direccion='calle 23',
            rfc='123123',
            razon_social='razon social',
            email='proveedor@gmail.com'
        )
        data = {
            'proveedor': '1',
            'fecha_compra': '2018-04-04'

        }
        self.client.post(reverse('compras:agregar_compra'), data)

        # Crear orden de compra
        data = {
            'material': Material.objects.first().id,
            'fecha_cad': '2019-04-04',
            'cantidad': '2',
            'costo': '30',
            'compra': Compra.objects.first().id
        }
        self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data)

        #Crear Receta
        data = {
            'nombre':'Receta Semi-Terminado',
            'codigo':'2342',
            'cantidad':'1',
            'duracion_en_dias':'10',

        }

        self.client.post(reverse('recetas:agregar_receta'), data)
        #Crear materiales de la receta
        data = {
            'material': str(Material.objects.first().nombre),
            'cantidad': '1',
        }

        self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta':Receta.objects.first().id}), data)
        #Crear Orden De Trabajo
        data = {
            'receta': Receta.objects.first().id,
            'fecha_fin': '2018-10-10',
            'multiplicador': '1',
        }
        self.client.post(reverse('ordenes:ordenes'), data)
        #Terminar Orden De Trabajp
        data = {
            'id': Orden.objects.first().id,
            'estatus': '2',
        }
        self.client.post(reverse('ordenes:terminar_orden'), data)

    #Test AC 34.1 Producto Semi-Terminado
    def testVerCostoReceta(self):
        #Checar el precio del producto semi-terimando con el costo de la orden que fue originada
        self.assertEqual(RecetaInventario.objects.first().costo, 15)
