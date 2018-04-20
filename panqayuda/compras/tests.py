from django.test import TestCase
from django.urls import reverse
from compras.models import Compra
import datetime
from django.contrib.auth.models import User, Group
from django.utils import timezone
from proveedores.models import Proveedor
from materiales.models import Material, Unidad, MaterialInventario
#test US 10
class TestListaCompras(TestCase):

    def setUp(self):
        #El setup crea un usuario e inicia sesion para poder iniciar con los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        #Se crea un proveedor
        self.proveedor = Proveedor.objects.create(
            nombre="TestLista",
            telefono=4151043944,
            direccion="Aqui mero patatero",
            rfc="12342121",
            razon_social="Un tipazo",
            email="test@ejemplo.com"
        )
        #Se crea una compra
        self.compra = Compra.objects.create(proveedor=self.proveedor, fecha_compra="2059-03-03 12:31:06-05")
        #Se crea un material catalogo
        self.material = Material.objects.create(nombre="Material Test", codigo=12344)
        #Se agrega una unidad
        self.unidad = Unidad.objects.create(nombre="Unidad")
        #Se crea material al inventario
        materialinv = MaterialInventario.objects.create(
            material=self.material,
            compra=self.compra,
            unidad_entrada=self.unidad,
            cantidad=12,
            cantidad_disponible=12,
            costo=100,
            fecha_cad="2059-03-03 12:31:06-05"
        )


    def test_ac1_Existe_la_vista_de_listado(self):
        resp = self.client.get(reverse('compras:compras'))
        #El codigo de respuesta debe de ser exitoso
        self.assertEqual(resp.status_code, 200)

    def test_ac2_Muestra_las_compras_correctas(self):
        #Se checa si existe el objeto compra
        self.assertEqual(Compra.objects.count(), 1)
        resp = self.client.get(reverse('compras:compras'))
        #El codigo de repuesta debe de ser exitoso
        self.assertEqual(resp.status_code, 200)
        #El contexto debe mostrar la compra
        self.assertEqual(resp.context['compras'].count(), 1)
        #self.assertEqual(resp.context['compras'].proveedor, "TestLista")

    def test_ac3_La_vista_detalle_existe(self):
        self.assertEqual(Compra.objects.count(), 1)
        id = Compra.objects.first()
        data = {'id_compra':id.pk}
        resp = self.client.post(reverse('compras:lista_detalle_compra'), data)
        self.assertEqual(resp.status_code, 200)

    def test_ac4_lista_detalle_es_correcta(self):
        self.assertEqual(Compra.objects.count(), 1)
        id = Compra.objects.first()
        data = {'id_compra':id.pk}
        resp = self.client.post(reverse('compras:lista_detalle_compra'), data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['compra'].proveedor, id.proveedor)

    #US 7
    def test_ac1_compra_se_crea(self):
        cuenta_prepost = Compra.objects.count()
        data = { 'fecha_compra':'2059-03-03', 'proveedor':self.proveedor.id }
        resp = self.client.post(reverse('compras:agregar_compra'), data)
        cuenta_postpost = Compra.objects.count()
        self.assertEqual(cuenta_prepost+1, cuenta_postpost)

    def test_ac2_sin_proveedor(self):
        cuenta_prepost = Compra.objects.count()
        data = {'fecha_compra':'2059-03-03'}
        resp = self.client.post(reverse('compras:agregar_compra'), data)
        cuenta_postpost = Compra.objects.count()
        self.assertEqual(cuenta_prepost, cuenta_postpost)

    def test_ac6_ver_costo_compra(self):
        response = self.client.get(reverse('compras:agregar_materias_primas_a_compra', kwargs={'id_compra':self.compra.id}))
        data = {'material':self.material.id, 'fecha_cad':'2059-03-03', 'cantidad':'5', 'unidad_entrada':self.unidad.id, 'porciones':'999', 'costo':'50',  'compra':self.compra.id}
        resp = self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data)
        data2 = {'material':self.material.id, 'fecha_cad':'2059-03-03', 'cantidad':'5', 'unidad_entrada':self.unidad.id, 'porciones':'999', 'costo':'45',  'compra':self.compra.id}
        resp2 = self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data2)
        response = self.client.get(reverse('compras:agregar_materias_primas_a_compra', kwargs={'id_compra':self.compra.id}))
        self.assertContains(response, 'Total')
        self.assertContains(response, '95')

    def test_ac3_agregar_materia_prima(self):
        cuenta_prepost=MaterialInventario.objects.filter(compra=self.compra.id).count()
        data = {'material':self.material.id, 'fecha_cad':'2059-03-03', 'cantidad':'10', 'unidad_entrada':self.unidad.id, 'porciones':'200', 'costo':'100',  'compra':self.compra.id}
        resp = self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data)
        cuenta_postpost=MaterialInventario.objects.filter(compra=self.compra.id).count()
        self.assertEqual(cuenta_prepost+1, cuenta_postpost)

    def test_ac4_cantidad_negativa(self):
        cuenta_prepost=MaterialInventario.objects.filter(compra=self.compra.id).count()
        data = {'material':self.material.id, 'fecha_cad':'2059-03-03', 'cantidad':'-10', 'unidad_entrada':self.unidad.id, 'porciones':'200', 'costo':'100',  'compra':self.compra.id}
        resp = self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data)
        cuenta_postpost=MaterialInventario.objects.filter(compra=self.compra.id).count()
        self.assertEqual(cuenta_prepost, cuenta_postpost)


    def test_ac5_ver_lista_materias_primas_en_compra(self):
        url = "/compras/agregar_materias_primas_a_compra/"+str(self.compra.id)
        response = self.client.get(url)
        self.assertNotContains(response, '999') #no se puede usar unidades o nombre del material porque siempre aparecen por el select
        data = {'material':self.material.id, 'fecha_cad':'2059-03-03', 'cantidad':'999', 'unidad_entrada':self.unidad.id, 'porciones':'999', 'costo':'999',  'compra':self.compra.id}
        resp = self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data)
        response = self.client.get(url)
        self.assertContains(response, '999')

class TestEliminarCompra(TestCase):

    def setUp(self):
        #El setup crea un usuario e inicia sesion para poder iniciar con los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        #Se crea un cliente
        self.client.login(username='temporary', password='temporary')
        #Se crea un proveedor
        proveedor = Proveedor.objects.create(
            nombre="TestLista",
            telefono=4151043944,
            direccion="Aqui mero patatero",
            rfc="12342121",
            razon_social="Un tipazo",
            email="test@ejemplo.com"
        )
        #Se crea una compra
        compra = Compra.objects.create(
            proveedor=proveedor,
            fecha_compra="2059-03-03 12:31:06-05"
        )
        #Se guarda la compra
        compra.save()

    def test_borrar_compra(self):
        self.assertEqual(Compra.objects.count(), 1)
        objetos = Compra.objects.first()
        #Se elimina mandando una peticion GET al url de eliminar compra
        self.client.get(reverse('compras:eliminar_compra', kwargs={'id_compra':objetos.id}))
        #Se checa que se haya eliminado el objeto compra
        self.assertEqual(Compra.objects.filter(deleted_at__isnull=True).count(), 0)





    #             cuenta_prepost=MaterialInventario.objects.filter(compra=self.compra.id).count()
    #             data = {'material':self.material.id, 'fecha_cad':'2059-03-03', 'cantidad':'10', 'unidad_entrada':self.unidad.id, 'porciones':'200', 'costo':'100',  'compra':self.compra .id}
    #             resp = self.client.post(reverse('compras:agregar_materia_prima_a_compra'), data)
    #             cuenta_postpost=MaterialInventario.objects.filter(compra=self.compra.id).count()
    #             self.assertEqual(cuenta_prepost+1, cuenta_postpost)
    # # Create your tests here.
