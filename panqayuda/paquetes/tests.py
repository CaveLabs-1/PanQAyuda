from django.test import TestCase
from paquetes.models import Paquete, RecetasPorPaquete
from recetas.models import Receta
import datetime
from django.urls import reverse

#Test creado por Manuel
class TestEditarPaqueteCatalogo(TestCase):

    def setUp(self):
        return Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    def crear_Paquete(self):
        return Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)

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
        data2 = {'nombre':"Paquete editado", 'precio':12, 'estatus':1}
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

    


# Create your tests here.
