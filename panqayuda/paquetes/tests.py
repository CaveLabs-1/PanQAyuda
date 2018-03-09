from django.test import TestCase
from paquetes.models import Paquete, RecetasPorPaquete
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


#US24
class TestEditarPaqueteCatalogo(TestCase):
    #Crear objetos de prueba
    def setUp(self):
        #Crear receta de prueba
        Receta.objects.create(nombre="Receta de prueba", precio=100)

    def crear_Paquete(self):
        return Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)

    def test_ac_24_1_agregar_paquete_lista_paquetes(self):
        #Post con información correcta
        data={'nombre': 'Rudy', 'precio': '1.50'}
        self.client.post(reverse('paquetes:agregar_paquete'), data)

        #Verificar que se creó el paquete
        self.assertEqual(Paquete.objects.count(), 2)

        #Verificar que aparece en la lista de paquetes
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(len(resp.context['lista_de_paquetes']),1)
        self.assertEqual(resp.context['lista_de_paquetes'][0].nombre, "Rudy")

    def test_ac_24_2_precio_incorrecto(self):
        #Post con precio 0
        data={'nombre':'Rudy', 'precio':0}
        resp = self.client.post(reverse('paquetes:agregar_paquete'),data)
        #Verificar que no se haya agregado
        self.assertEqual(Paquete.object.count(),0)
        #Verificar mensaje de error
        self.assertFormError(resp, 'forma', 'precio', 'El precio del paquete debe ser mayor a 0.')

        #Post con precio negativo
        data={'nombre':'Edgar', 'precio':'-25.53'}
        resp = self.client.post(reverse('paquetes:agregar_paquete'),data)
        #Verificar que no se haya agregado
        self.assertEqual(Paquete.object.count(),0)
        #Verificar mensaje de error
        self.assertFormError(resp, 'forma', 'precio', 'El precio del paquete debe ser mayor a 0.')

    def test_ac_24_3_paquete_mismo_nombre(self):
        #Intentar crear paquete con el mismo nombre
        data={'nombre':'Paquete de prueba', 'precio':100}
        resp = self.client.post((reverse('paquetes:agregar_paquete')))

        #Verificar que no se haya creado el paquete
        self.assertEqual(Paquete.objects.count(), 1)

        #Verificar mensaje de error
        self.assertFormError(resp, 'forma', 'nombre', 'Ya hay un paquete con este nombre')

        #Verificar case sensitive
        data = {'nombre': 'PAQUETE de PRUEBA', 'precio': 100}
        resp = self.client.post(reverse('paquetes:agregar_paquete'),data)

        # Verificar que no se haya creado el paquete
        self.assertEqual(Paquete.objects.count(), 1)

        # Verificar mensaje de error
        self.assertFormError(resp, 'forma', 'nombre', 'Ya hay un paquete con este nombre')

    def test_ac_24_4_agregar_receta_paquete(self):
        #Crear paquete de prueba
        paquete = self.crear_Paquete()
        #Post correcto para agregar receta a un paquete
        data= {'receta':'1','cantidad':'10','paquete':paquete.id}
        self.client.post(reverse('paquetes:agregar_receta_a_paquete'),data)

        #Verificar lista de recetas
        resp=self.client.get(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':1}))
        self.assertEqual(len(resp.context['recetas_por_paquete']),1)

    def test_ac_24_5_agregar_receta_repetida_a_paquete(self):
        #Crear paquete de prueba
        paquete = self.crear_Paquete()
        receta = Receta.objects.last()
        #Agregar receta a paquete
        paquete.recetas.add(receta)

        #Verificar que se hizo la relación
        self.assertEqual(paquete.recetas.count(),1)

        #Intentar volver a crear la relacion
        data= {'receta':receta.id,'cantidad':'10','paquete':paquete.id}
        self.client.post(reverse('paquetes:agregar_receta_a_paquete'))

        #Verificar que no se hizo la relación
        self.assertEqual(paquete.recetas.count(),1)

    def test_ac_24_6_recetas_de_paquete_no_disponibles(self):
        #Crear paquete y hacer relación
        paquete = self.crear_Paquete()
        receta = Receta.objects.last()
        paquete.recetas.add(receta)

        #Verificar que ya no esté disponible
        resp = self.client.get(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        self.assertEqual(len(resp.context['recetas']),0)

    def test_ac_24_7_cantidad_receta_negativa(self):
        #Crear paquete para probar
        paquete = self.crear_Paquete()
        receta = Receta.objects.last()

        #Post con cantidad 0
        data= {'receta':receta.id,'cantidad':'0','paquete':paquete.id}
        self.client.post(reverse('paquetes:agregar_receta_a_paquete',kwargs={'id_paquete':paquete.id}),data)
        #Verificar que no se hizo la relación
        self.assertEqual(Paquete.objects.last().recetas.count(),0)

        #Post con cantidad negativa
        data= {'receta':receta.id,'cantidad':'-100','paquete':paquete.id}
        self.client.post(reverse('paquetes:agregar_receta_a_paquete', kwargs={'id_paquete':paquete.id}),data)

        #Verificar que no se hizo la relación
        self.assertEqual(Paquete.objects.last().recetas.count(),0)

    #def test_rbac(self):


    def test_ac_24_9_paquetes_no_activos(self):
        #Crear paquete de prueba y 'borrarlo'
        paquete = self.crear_Paquete()
        paquete.deleted_at=datetime.datetime.today()
        paquete.estatus=0
        paquete.save()

        #Verificar que al intentar verlo regresa un 404.
        resp = self.client.get(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        self.assertEqual(resp.status_code, 404)

    def test_ac_24_10_recetas_no_activas_agregar_paquete(self):
        #Crear paquete de prueba
        paquete = self.crear_Paquete()

        #'Eliminar' receta existente
        receta = Receta.objects.last()
        receta.status=0
        receta.deleted_at=datetime.datetime.today()

        #Verificar que la receta no se muestra
        resp = self.client.get(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        self.assertEqual(len(resp.context['recetas']),0)

# Create your tests here.
