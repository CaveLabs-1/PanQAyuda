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
        #El setup crea un usuario e inicia sesion para poder iniciar con los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    #existe la vista
    def test_valid_session(self):
        session = self.client.session

    def test_ac1_existe_la_vista_html(self):
        #Guarda en una variable el resultado de acceder al url de materiales
        resp = self.client.get(reverse('materiales:materiales'))
        #En este caso no debe de haber ningun material en el contexto ya que no se ha creado uno
        self.assertEqual(len(resp.context['materiales']),0)
        #Se checa que el codigo de estatus sea de 200
        self.assertEqual(resp.status_code, 200)

    def test_ac2_existe_la_vista_con_algo(self):
        #Crea un objeto de material
        Unidad.objects.create(id=1, nombre="kg")
        Material.objects.create(nombre="Testerino", codigo="1313", unidad_entrada_id=1, unidad_maestra_id=1)
        #Guarda en una variable el resultado de acceder al url
        resp = self.client.get(reverse('materiales:materiales'))
        #Como se creo una materia, ahora si debe de haber una en el contexto
        self.assertEqual(len(resp.context['materiales']),1)
        #Se checa el estatus de la respuesta que debe ser exitoso
        self.assertEqual(resp.status_code, 200)

    def test_ac3_la_tabla_no_imprime_objetos_con_estatus_no_disponible(self):
        #Se checa que no exista ningun material
        self.assertEqual(Material.objects.count(), 0)
        #Se crea un material
        Unidad.objects.create(id=1, nombre="kg")
        Material.objects.create(nombre="Test ac3", codigo="123456789", status=0,unidad_entrada_id=1, unidad_maestra_id=1)
        #Se checa que se haya creado exitosamente
        self.assertEqual(Material.objects.count(), 1)
        #Se guarda en una variable el resultado de acceder al url
        resp = self.client.get(reverse('materiales:materiales'))
        #Se checa que no exista en el contexto el objeto con estatus 0
        self.assertEqual(len(resp.context['materiales']), 0)
        #La respuesta al acceder al url debe ser exitosa
        self.assertEqual(resp.status_code, 200)

    #se agrega exitosamente el material
    def test_ac4_se_agrega_material_y_se_muestra_en_la_tabla(self):
        #Se checa que no exista materia
        self.assertEqual(Material.objects.count(), 0)
        #Se guarda el resultado de acceder al url de materiales
        resp = self.client.get(reverse('materiales:materiales'))
        #Se checa que el contexto tambien este vacio
        self.assertEqual(len(resp.context['materiales']),0)
        #Se checa que la respuesta de estatus sea exitosa
        self.assertEqual(resp.status_code, 200)
        #Se crea una materia
        Unidad.objects.create(id=1, nombre="kg")
        Material.objects.create(nombre="Test ac4", codigo="123456789", status=1, unidad_entrada_id=1,
                                unidad_maestra_id=1)
        #Se guarda en una nueva variable la respuesta de acceder al url
        resp2 = self.client.get(reverse('materiales:materiales'))
        #Se checa que en el contexto ya este la materia que se creo
        self.assertEqual(len(resp2.context['materiales']),1)
        #La respuesta es exitosa
        self.assertEqual(resp2.status_code, 200)
        #Se crea otra materia
        Material.objects.create(nombre="Test ac4.2", codigo="123456789", status=1, unidad_entrada_id=1,
                                unidad_maestra_id=1)
        resp3 = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(len(resp3.context['materiales']),2)

class TestAgregarMateriaCatalogo(TestCase):

    def setUp(self):
        #El setup crea un usuario e inicia sesion para poder iniciar con los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_ac1_existe_vista_agregar(self):
        #self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(resp.status_code, 200)

    def test_ac2_se_agrega_el_material(self):
        #Se checa que no haya materias
        self.assertEqual(Material.objects.count(), 0)
        #Se guarda la informacion
        Unidad.objects.create(id=1, nombre="kg")
        data = {
            'nombre': 'Material',
            'codigo': '1223123',
            'equivale_entrada': '1',
            'unidad_entrada': '1',
            'equivale_maestra': '1',
            'unidad_maestra': 1
        }
        #Se manda la informacion al url con un POST y se crea una materia
        self.client.post(reverse('materiales:materiales'), data)
        #Se checa que se haya creado la materia
        self.assertEqual(Material.objects.count(), 1)

    def test_ac3_no_permite_agregar_material_sin_nombre(self):
        #Se checa que no exista una materia
        self.assertEqual(Material.objects.count(), 0)
        Unidad.objects.create(id=1, nombre="kg")
        data = {
            'nombre': '',
            'codigo': '1223123',
            'equivale_entrada': '1',
            'unidad_entrada': '1',
            'equivale_maestra': '1',
            'unidad_maestra': 1
        }
        #Se manda el data por medio de POST al urll que crea materias
        self.client.post(reverse('materiales:materiales'), data)
        #Se checa que no se haya creado la materia erronea
        self.assertEqual(Material.objects.count(), 0)

    def test_ac4_no_permite_material_sin_codigo(self):
        #Se checq que no exista la materia
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac 4"}
        self.client.post(reverse('materiales:materiales'), data)
        #Se manda informacion erronea y se espera que no se cree la materia
        self.assertEqual(Material.objects.count(), 0)

    def test_ac5_no_excede_10_caracteres_codigo(self):
        #Se checa que no haya materia existente
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac5", 'codigo':12345678910}
        self.client.post(reverse('materiales:materiales'), data)
        #Se manda informacion erronea y se esera que no se cree la materia
        self.assertEqual(Material.objects.count(), 0)

    def test_ac6_no_excede_100_caracteres_nombre(self):
        #Se checa que no exsita la materia existente
        self.assertEqual(Material.objects.count(), 0)
        data = {'nombre':"Test ac6 excede el limite de 100 caracteres y no permite que se guarde el nomrbe y no se guarda en la base de datos", 'codigo':123456789}
        self.client.post(reverse('materiales:materiales'), data)
        #En el data se mando un nombre con mas de 100 caracteres y se espera que no se guarde el objeto
        self.assertEqual(Material.objects.count(), 0)

    def test_ac7_codigo_no_alfa_numerico(self):
        #Se checa que no exista materia
        self.assertEqual(Material.objects.count(), 0)
        Unidad.objects.create(id=1, nombre="kg")
        data = {
            'nombre': 'Material',
            'codigo': '1223123',
            'equivale_entrada': '1',
            'unidad_entrada': '1',
            'equivale_maestra': '1',
            'unidad_maestra': 1
        }
        self.client.post(reverse('materiales:materiales'), data)
        #Se checa que el codigo acepte codigos alfanumericos y se crea la materia
        self.assertEqual(Material.objects.count(), 1)

#Casos de uso US54
class TestListaUnidades(TestCase):

    def setUp(self):
        #El setup crea un usuario e inicia sesion para poder iniciar con los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_ac1_existe_la_vista_lista(self):
        resp = self.client.get(reverse('materiales:lista_unidades'))
        #El codigo de repsuesta debe de ser exitoso, es decir, 200
        self.assertEqual(resp.status_code, 200)

    def test_ac2_se_muestra_la_lista_con_unidades_agregadas(self):
        #Se checa que la nunidad no exista
        self.assertEqual(Unidad.objects.count(), 0)
        #Se crea una nueva unidad
        Unidad.objects.create(nombre="ac2")
        #Se checa que se haya creado
        self.assertEqual(Unidad.objects.count(), 1)
        resp = self.client.get(reverse('materiales:lista_unidades'))
        #Se checa que en el contexto de la tabla se vea la unidad que se creo
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

    #Crea unidad
    def crear_unidad(self):
        return Unidad.objects.create(id=1, nombre="Unidad")

    #Crea unidad auxiliar
    def crear_unidad2(self):
        return Unidad.objects.create(id=2, nombre="Unidad auxiliar")

    #Verifica que la vista para modificar unidad exista
    def test_vista_modificar_unidad(self):
        self.crear_unidad()
        resp = self.client.get(reverse('materiales:modificar_unidad', kwargs={'id_unidad':1}))
        self.assertEqual(resp.status_code, 302)

    #Verifica que pueda modificar la unidad existente
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

    # Valida que el campo de nombre no llegue vacio
    def test_errorNombreVacia(self):
        self.crear_unidad()
        data = {'nombre':''}
        resp = self.client.post(reverse('materiales:modificar_unidad', kwargs={'id_unidad':1}), data)
        #Checar que solo hay una y no mas
        self.assertEqual(Unidad.objects.count(), 1)

    # Valida que la unidad que se desea crear no exista en la base de datos
    def test_prohibeCrearUnidadExistente(self):
        unidad1 = self.crear_unidad()
        unidad2 = self.crear_unidad2()


        data = {'nombre':"Unidad"}
        self.client.post(reverse('materiales:modificar_unidad', kwargs={'id_unidad':2}), data)
        resp = self.client.get(reverse('materiales:modificar_unidad', kwargs={'id_unidad':2}))
        #Verificar que una nueva unidad no se haya creado
        self.assertTrue(Unidad.objects.all().count() == 2)
#

#Caso de uso US14
class TestListaMateriaPrima(TestCase):

    def creacion1(self):
        #Para poder crear material en invetario es necesario crear una unidad, un material catalogo, crear un proveedor, y una orden de compra
        Unidad.objects.create(nombre="kg")
        unidad = Unidad.objects.first()
        material = Material.objects.first()
        proveedor = Proveedor.objects.first()
        compra = Compra.objects.first()
        inventario2 = MaterialInventario.objects.create(
            id=20,
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
        #El setup crea un usuario e inicia sesion para poder iniciar con los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        unidad = Unidad.objects.create(
            nombre="kilogramo", id=3)
        unidad.save()
        material = Material.objects.create(id=50, nombre="Testerino", codigo="1313", status=0, unidad_entrada_id=3, unidad_maestra_id=3)
        material = Material.objects.create(id=55, nombre="Testerino", codigo="1313", status=1, unidad_entrada_id=3, unidad_maestra_id=3)
        material.save()
        proveedor = Proveedor.objects.create(
            nombre="Manuel Flores",
            telefono='4151046632',
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
            id=33,
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
        #Se checq eue el material este vacio
        self.assertEqual(MaterialInventario.objects.count(), 1)
        resp = self.client.get(reverse('materiales:materiales'))
        #Se checa que el codigo de respuesta sea exitoso
        self.assertEqual(resp.status_code, 200)
        #Como se creo una materia, se debe de observar en el contexto
        self.assertEqual(resp.context['materiales'].count(), 1)

    def test_ac3_no_muestra_lista_de_materiales_estatus_cero(self):
        #Se crean dos materiales en inventario y se checan en existencia
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



#tests dle caso de uso 12
class TestEditarMateriaCatalogo(TestCase):

    def setUp(self):
        #El setup crea un usuario e inicia sesion para poder iniciar con los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        Unidad.objects.create(nombre="kg", id=1)
        Material.objects.create(nombre="Test", codigo="1313", unidad_entrada_id=1, unidad_maestra_id=1)


    def test_ac1_existe_la_vista(self):
        objeto = Material.objects.first()
        id = objeto.id
        resp=self.client.post(reverse('materiales:editar_material', kwargs={'id_material':id}))
        self.assertTrue(resp.status_code == 200)

    def test_ac2_la_vista_corresponde_al_item(self):
        objeto = Material.objects.first()
        id = objeto.id
        resp = self.client.get(reverse('materiales:editar_material', kwargs={'id_material':id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['material'].nombre, "Test")

    def test_ac3_No_cambia_el_nombre_a_uno_existente(self):
        objeto = Material.objects.first()
        id = objeto.id
        Material.objects.create(nombre="Test2", codigo='122212', unidad_entrada_id=1, unidad_maestra_id=1)
        self.assertEqual(Material.objects.count(), 2)
        data = {'nombre':"Test2", 'codigo':1221212}
        resp = self.client.post(reverse('materiales:editar_material', kwargs={'id_material':id}), data)
        self.assertEqual(Material.objects.first().nombre, "Test")

    def test_ac4_No_se_guarda_sin_nombre(self):
        objeto = Material.objects.first()
        id = objeto.id
        Material.objects.create(nombre="Test2", codigo='122212', unidad_entrada_id=1, unidad_maestra_id=1)
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

    #Generación para el ambiente de pruebas de eliminar materia prima
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        Unidad.objects.create(id=66, nombre="kg")
        material = Material.objects.create(nombre='Huevo', codigo='122212', unidad_entrada_id=66, unidad_maestra_id=66)
        material.save()

    #Test para eliminar la materia prima
    def test_borrar_material(self):
        self.assertEqual(Material.objects.count(), 1)
        #Obtienes el objeto material
        objetos = Material.objects.first()
        #Se utiliza eliminar_material
        self.client.get(reverse('materiales:eliminar_material', kwargs={'id_material':objetos.id}))
        #Se busca que no haya con cambio vacío de deleted_at
        self.assertEqual(Material.objects.filter(deleted_at__isnull=True).count(), 0)

#Test US 34
class TestVerCostoMaterial(TestCase):
    # Setup de AC 34.1 de Materiales
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                        is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        #Agregar Unidad
        Unidad.objects.create(id=67, nombre="kg")
        material = Material.objects.create(nombre='Huevo', codigo='122212', unidad_entrada_id=67, unidad_maestra_id=67)
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



    # AC 34.1 de Materiales
    def testVerCostoMaterial(self):
        #Crear orden de compra

        Proveedor.objects.create(
            nombre='ALejandro',
            telefono='4424708341',
            direccion='calle 23 #1',
            rfc='ASD123ASDQWEA',
            razon_social='EMPRESA',
            email='ale@hot.com'
        )
        Compra.objects.create(
            proveedor=Proveedor.objects.all().first(),
            fecha_compra='2018-10-10'
        )


        data = {
            'material': Material.objects.all().first().id,
            'fecha_cad': '2019-04-04',
            'cantidad': '2',
            'costo': '30',
            'compra': Compra.objects.all().first().id
        }



        self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data)
        # Costo Unitario que debe aparecer cuando se guarde la forma
        costo_unitario = int((data['costo']))/int((data['cantidad']))
        # Checar en el template que el costo unitario mostrado es el mismo
        resp = self.client.get('/materiales/#modal_detalle')
        for material in resp.context['materiales']:
            self.assertEqual(int(costo_unitario), int(material.costo_unitario))


