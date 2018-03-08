from django.test import TestCase
from paquetes.models import Paquete, RecetasPorPaquete, PaqueteInventario
from recetas.models import Receta
import datetime
from django.urls import reverse

#Test creado por Manuel y David
# jaja Bromi
class TestEditarPaqueteCatalogo(TestCase):

    def setUp(self):
        return Receta.objects.create(nombre="Paquete de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    def crear_Paquete(self):
        return Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)

    def crear_Paquete2(self):
        return Paquete.objects.create(id=2, nombre="Paquete auxiliar", precio=11, estatus=1)

    def crear_relacion_paquete_receta(self, receta, paquete):
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta, cantidad=2)

    def test_vista_editar_paquete(self):
        self.crear_Paquete()
        resp = self.client.get(reverse('paquetes:editar_paquete', kwargs={'id_paquete':1}))
        self.assertEqual(resp.status_code, 200)

    def test_ac_25_SePuedeEditarUnPaqueteDelCatalogo(self):
        #Checar si la base de datos esta vacia de paquetes
        self.assertEqual(Paquete.objects.count(), 0)
        #Se agrega la info basica para un paquete
        data1 = {'nombre':"Paquete prueba", 'precio':11}
        self.client.post(reverse('paquetes:agregar_paquete'), data1)
        #Se guarda un nuevo paquete sin recetas
        #en data2 se guarda el edit del paquete
        data2 = {'nombre':"Paquete editado", 'precio':12}
        #se manda a la ruta
        self.client.post(reverse('paquetes:editar_paquete', kwargs={'id_paquete':1}), data2)
        self.assertEqual(Paquete.objects.count(), 1)

    def test_ac_25_RegresaMensajeDeErrorAlDejarCampoDeNombreVacio(self):
        self.crear_Paquete()
        data = {'precio':'10'}
        resp = self.client.post(reverse('paquetes:editar_paquete', kwargs={'id_paquete':1}), data)

        self.assertEqual(Paquete.objects.count(), 1)
        self.assertFormError(resp, 'form', 'nombre', "Este campo no puede ser vacio")

    def test_ac_25_RegresaMensajeDeErrorAlDejarCampoDePrecioVacio(self):
        self.crear_Paquete()
        data = {'nombre':'Test Precio'}
        resp = self.client.post(reverse('paquetes:editar_paquete', kwargs={'id_paquete':1}), data)

        self.assertEqual(Paquete.objects.count(), 1)
        self.assertFormError(resp, 'form', 'precio', "Este campo no puede ser vacio")

    def test_ac_25_NoPermiteGuardarUnaOrdenConPrecioNoNumerico(self):
        data = {'nombre':"testerino", 'precio':"precio :v"}
        self.client.post(reverse('paquetes:editar_paquete', kwargs={'id_paquete':1}), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_25_NoPermitirQueAcepteNumerosNegativosEnElPrecio(self):
        data = {'nombre':"testerongo", 'precio':"-15"}
        self.client.post(reverse('paquetes:editar_paquete', kwargs={'id_paquete':1}), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_25_NoPermitePonerUnNombreDeUnPaqueteYaExistente(self):
        paquete1 = self.crear_Paquete()
        paquete2 = self.crear_Paquete2()

        data = {'nombre':"Paquete de Prueba", 'precio':12}
        self.client.post(reverse('paquetes:editar_paquete', kwargs={'id_paquete':2}), data)
        resp = self.client.get(reverse('paquetes:editar_paquete', kwargs={'id_paquete':2}))
        paquete = resp.context['paquete']

        nombre1 = paquete1.nombre
        nombre2 = paquete.nombre
        self.assertFalse(nombre1 == nombre2)

class TestAgregarPaqueteInventario(TestCase):

    def setUp(self):
        return Receta.objects.create(nombre="Paquete de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    def crear_Paquete(self):
        return Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)

    def crear_Paquete2(self):
        return Paquete.objects.create(id=2, nombre="Paquete auxiliar", precio=11, estatus=1)

    def crear_relacion_paquete_receta(self, receta, paquete):
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta, cantidad=2)

    def test_vista_agregar_paquete_inventario(self):
        self.crear_Paquete()
        resp = self.client.get(reverse('paquetes:agregar_inventario'))
        self.assertEqual(resp.status_code, 200)

    def test_ac_21_2_Campo_de_nombre_no_puede_ser_vacio(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"", 'cantidad':"1", 'fecha_cad':"03-07-1997", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_21_3_No_permite_dejar_campo_cantidad_vacio(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"Testerino", 'cantidad':"", 'fecha_cad':"03-03-1997", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_21_4_No_permite_guardar_con_campo_fecha_vacio(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"Testerino", 'cantidad':"10", 'fecha_cad':"", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_21_5_No_Permite_cantidad_negativa(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"Testerino", 'cantidad':"-12", 'fecha_cad':"03-03-1997", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_21_6_No_permite_fechas_inexistentes(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"Testerino", 'cantidad':"10", 'fecha_cad':"40-40-1997", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_21_7_Solo_permite_formato_de_fecha_en_campo_fecha(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"Testerino", 'cantidad':"10", 'fecha_cad':"Martes 10", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_21_8_Solo_permite_numeros_enteros_en_cantidad(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"Testerino", 'cantidad':"10.11", 'fecha_cad':"03-03-1997", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 0)

    def test_ac_21_9_Se_agrega_exitosamente_el_paquete(self):
        self.assertEqual(Paquete.objects.count(), 0)
        data = {'nombre':"Testerino", 'cantidad':"10", 'fecha_cad':"03-03-1997", 'estatus':"1"}

        self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 1)

# Create your tests here.
