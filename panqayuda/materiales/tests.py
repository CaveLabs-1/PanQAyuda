from django.test import TestCase
from django.urls import reverse
from materiales.models import Material
from materiales.models import Unidad
from materiales.models import MaterialInventario
from compras.models import Compra
from proveedores.models import Proveedor
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group

#test agregar materia prima US 11
class TestListaMaterialCatalogo(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    #existe la vista
    def test_valid_session(self):
        session = self.client.session

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
        self.assertEqual(Material.objects.count(), 0)
        Material.objects.create(nombre="Test ac3", codigo=123456789, status=0)
        self.assertEqual(Material.objects.count(), 1)
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

class TestAgregarMateriaCatalogo(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_ac1_existe_vista_agregar(self):
        #self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_se_agrega_el_material(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac2", 'codigo':123456789}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 1)

    def test_ac3_no_permite_agregar_material_sin_nombre(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'codigo':123456789}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac4_no_permite_material_sin_codigo(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac 4"}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac5_no_excede_10_caracteres_codigo(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac5", 'codigo':12345678910}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac6_no_excede_100_caracteres_nombre(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac6 excede el limite de 100 caracteres y no permite que se guarde el nomrbe y no se guarda en la base de datos", 'codigo':123456789}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 0)

    def test_ac7_codigo_no_alfa_numerico(self):
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac7", 'codigo':"12d4s6Q890"}
        self.client.post(reverse('materiales:materiales'), data)
        self.assertEqual(Material.objects.count(), 1)

#Casos de uso US54
class TestListaUnidades(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_ac1_existe_la_vista_lista(self):
        resp = self.client.get(reverse('materiales:lista_unidades'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_se_muestra_la_lista_con_unidades_agregadas(self):
        self.assertEqual(Unidad.objects.count(), 0)
        Unidad.objects.create(nombre="ac2")
        self.assertEqual(Unidad.objects.count(), 1)
        resp = self.client.get(reverse('materiales:lista_unidades'))
        self.assertEqual(len(resp.context['unidades']), 1)

    def test_ac3_existe_vista_agregar(self):
        data = {'nombre':"ac3"}
        resp = self.client.get(reverse('materiales:lista_unidades'), data)
        self.assertEqual(resp.status_code, 200)

    def test_ac4_no_se_agrega_la_unidad(self):
        self.assertEqual(Unidad.objects.count(), 0)
        data = {'nombre':"ac4"}
        self.client.post(reverse('materiales:lista_unidades'), data)
        self.assertEqual(Unidad.objects.count(), 1)

    def test_ac5_no_se_agrega_el_nombre(self):
        self.assertEqual(Unidad.objects.count(), 0)
        data = {'nombre':""}
        self.client.post(reverse('materiales:lista_unidades'), data)
        self.assertEqual(Unidad.objects.count(), 0)

#Caso de uso US55
class TestModificarUnidades(TestCase):

    #Revisar que la sesión exista
    def test_valid_session(self):
        session = self.client.session

    def crear_unidad(self):
        return Unidad.objects.create(id=1, nombre="Unidad")

    def crear_unidad2(self):
        return Unidad.objects.create(id=2, nombre="Unidad auxiliar")

    def test_vista_modificar_unidad(self):
        self.crear_unidad()
        resp = self.client.get(reverse('materiales:modificar_unidad', kwargs={'id_unidad':1}))
        self.assertEqual(resp.status_code, 200)

    def test_modificarUnidad(self):
        #Checar si la base de datos esta vacia de unidades
        self.assertEqual(Unidad.objects.count(), 0)
        #Se agrega la info basica para una unidad
        self.crear_unidad()
        #Se guarda una nueva unidad
        #en data2 se guarda el edit de la unidad
        data2 = {'nombre':"Gramos"}
        #se manda a la ruta
        self.client.post(reverse('materiales:modificar_unidad', kwargs={'id_unidad':1}), data2)
        self.assertEqual(Unidad.objects.count(), 1)

    def test_errorNombreVacia(self):
        self.crear_unidad()
        data = {'nombre':''}
        resp = self.client.post(reverse('materiales:modificar_unidad', kwargs={'id_unidad':1}), data)

        self.assertEqual(Unidad.objects.count(), 1)
        self.assertFormError(resp, 'form', 'nombre', "Este campo no puede ser vacío")

    def test_prohibeCrearUnidadExistente(self):
        unidad1 = self.crear_unidad()
        unidad2 = self.crear_unidad2()

        data = {'nombre':"Unidad 1"}
        self.client.post(reverse('materiales:modificar_unidad', kwargs={'id_unidad':2}), data)
        resp = self.client.get(reverse('materiales:modificar_unidad', kwargs={'id_unidad':2}))
        unidad = resp.context['unidad']

        nombre1 = unidad1.nombre
        nombre2 = unidad.nombre
        self.assertFalse(nombre1 == nombre2)
#

#Caso de uso US14
class TestListaMateriaPrima(TestCase):

    def creacion1(self):
        unidad = Unidad.objects.first()
        material = Material.objects.first()
        proveedor = Proveedor.objects.first()
        compra = Compra.objects.first()
        inventario2 = MaterialInventario.objects.create(
            material=material,
            compra=compra,
            unidad_entrada=unidad,
            cantidad=1,
            porciones_disponible=12,
            costo=120,
            fecha_cad="2059-03-03 12:31:06-05",
            estatus=0)
        inventario2.save()

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        unidad = Unidad.objects.create(
            nombre="kilogramo")
        unidad.save()
        material = Material.objects.create(
            nombre="buebito",
            codigo=122345)
        material.save()
        proveedor = Proveedor.objects.create(
            nombre="Manuel Flores",
            telefono=4151046632,
            direccion="Aqui mero patatero",
            rfc="testerino",
            razon_social="es un tipazo",
            email="mane@hotmail.com")
        proveedor.save()
        compra = Compra.objects.create(
            proveedor=proveedor,
            fecha_compra="2048-03-03 12:31:06-05")
        compra.save()
        inventario = MaterialInventario.objects.create(
            material=material,
            compra=compra,
            unidad_entrada=unidad,
            cantidad=1,
            porciones_disponible=12,
            costo=120,
            fecha_cad="2049-03-03 12:31:06-05")

    def test_ac1_existe_la_vista(self):
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_muestra_lista_de_materiales(self):
        self.assertEqual(MaterialInventario.objects.count(), 1)
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['materiales'].count(), 1)

    def test_ac3_no_muestra_lista_de_materiales_estatus_cero(self):
        self.assertEqual(MaterialInventario.objects.count(), 1)
        self.creacion1()
        self.assertEqual(MaterialInventario.objects.count(), 2)
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['materiales'].count(), 1)

    def test_ac4_existe_la_vista_detalle(self):
        self.assertEqual(MaterialInventario.objects.count(), 1)
        id = Material.objects.first()
        data = {'id_material':id.pk}
        resp = self.client.post(reverse('materiales:materiales_por_catalogo'), data)
        self.assertEqual(resp.status_code, 200)
        #self.assertEqual(resp.context['materiales'].count(), 1)


#tests dle caso de uso 12
class TestEditarMateriaCatalogo(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        Material.objects.create(nombre="Test", codigo=1000001)

    def test_ac1_existe_la_vista(self):
        objeto = Material.objects.first()
        id = objeto.id
        self.client.post(reverse('materiales:editar_material', kwargs={'id_material':id}))

    def test_ac2_la_vista_corresponde_al_item(self):
        objeto = Material.objects.first()
        id = objeto.id
        resp = self.client.get(reverse('materiales:editar_material', kwargs={'id_material':id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['material'].nombre, "Test")

    def test_ac3_No_cambia_el_nombre_a_uno_existente(self):
        objeto = Material.objects.first()
        id = objeto.id
        Material.objects.create(nombre="Test2", codigo=122212)
        self.assertEqual(Material.objects.count(), 2)
        data = {'nombre':"Test2", 'codigo':1221212}
        resp = self.client.post(reverse('materiales:editar_material', kwargs={'id_material':id}), data)
        self.assertEqual(Material.objects.first().nombre, "Test")

    def test_ac4_No_se_guarda_sin_nombre(self):
        objeto = Material.objects.first()
        id = objeto.id
        Material.objects.create(nombre="Test2", codigo=122212)
        self.assertEqual(Material.objects.count(), 2)
        data = {'nombre':"", 'codigo':1221212}
        resp = self.client.post(reverse('materiales:editar_material', kwargs={'id_material':id}), data)
        self.assertEqual(Material.objects.first().nombre, "Test")

class TestEliminarUnidad(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        unidad = Unidad.objects.create(nombre='caja')
        unidad.save()

    def test_borrar_unidad(self):
        self.assertEqual(Unidad.objects.count(), 1)
        objetos = Unidad.objects.first()
        self.client.get(reverse('materiales:eliminar_unidad', kwargs={'id_unidad':objetos.id}))
        self.assertEqual(Unidad.objects.filter(deleted_at__isnull=True).count(), 0)


class TestEliminarMaterial(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        material = Material.objects.create(nombre='Huevo', codigo=123)
        material.save()

    def test_borrar_material(self):
        self.assertEqual(Material.objects.count(), 1)
        objetos = Material.objects.first()
        self.client.get(reverse('materiales:eliminar_material', kwargs={'id_material':objetos.id}))
        self.assertEqual(Material.objects.filter(deleted_at__isnull=True).count(), 0)
