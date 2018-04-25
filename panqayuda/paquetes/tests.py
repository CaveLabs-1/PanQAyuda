from django.test import TestCase
from paquetes.models import Paquete, RecetasPorPaquete, PaqueteInventario
from django.urls import reverse
from recetas.models import Receta, RecetaInventario
import datetime
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.shortcuts import render

# #Test creado por Manuel
class TestEditarPaqueteCatalogo(TestCase):

    #Revisar que la sesión exista
    def test_valid_session(self):
        session = self.client.session

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
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
        self.assertFormError(resp, 'form', 'nombre', "Este campo no puede ser vacio")
        self.assertEqual(Paquete.objects.count(), 1)

    def test_ac_25_RegresaMensajeDeErrorAlDejarCampoDePrecioVacio(self):
        self.crear_Paquete()
        data = {'nombre':'Test Precio'}
        resp = self.client.post(reverse('paquetes:editar_paquete', kwargs={'id_paquete':1}), data)
        self.assertFormError(resp, 'form', 'precio', "Este campo no puede ser vacio")
        self.assertEqual(Paquete.objects.count(), 1)


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
#
#
class TestAgregarPaqueteInventario(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        receta = Receta.objects.create(nombre="Receta de prueba 1", duration=datetime.timedelta(days=1))
        receta_2 = Receta.objects.create(nombre="Receta de prueba 2", duration=datetime.timedelta(days=1))
        #Receta 1 en inventario que caduca en 5 día
        RecetaInventario.objects.create(nombre=receta, cantidad=3, fecha_cad=datetime.datetime.now()+datetime.timedelta(days=5))
        # Receta 1 en inventario que caduca en 1 día
        RecetaInventario.objects.create(nombre=receta, cantidad=3,fecha_cad=datetime.datetime.now() + datetime.timedelta(days=5))
        # Receta 1 en inventario que ya caducó
        RecetaInventario.objects.create(nombre=receta, cantidad=3, fecha_cad=datetime.datetime.now() - datetime.timedelta(days=5))
        #Receta 2 en inventario
        RecetaInventario.objects.create(nombre=receta_2, cantidad=15, fecha_cad=datetime.datetime.now() + datetime.timedelta(days=10))

        paquete = Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta, cantidad=5)
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta_2, cantidad=10)

    def crear_Paquete(self):
        return Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)

    def crear_Paquete2(self):
        return Paquete.objects.create(id=2, nombre="Paquete auxiliar", precio=11, estatus=1)

    def crear_relacion_paquete_receta(self, receta, paquete):
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta, cantidad=2)

    def test_vista_agregar_paquete_inventario(self):
        resp = self.client.get(reverse('paquetes:agregar_inventario'))
        self.assertEqual(resp.status_code, 200)

    def test_ac_21_2_Campo_de_nombre_no_puede_ser_vacio(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        data = {'cantidad':"1", 'fecha_cad':"2019-12-12"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(PaqueteInventario.objects.count(), 0)

    def test_ac_21_3_No_permite_dejar_campo_cantidad_vacio(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        data = {'nombre':"1", 'fecha_cad':"2019-12-12"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(PaqueteInventario.objects.count(), 0)

    def test_ac_21_4_No_permite_guardar_con_campo_fecha_vacio(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        data = {'nombre':"1", 'cantidad':"10"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(PaqueteInventario.objects.count(), 0)

    def test_ac_21_5_No_Permite_cantidad_negativa(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        data = {'nombre':"1", 'cantidad':"-12", 'fecha_cad':"2019-01-01"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(PaqueteInventario.objects.count(), 0)

    def test_ac_21_6_No_permite_fechas_inexistentes(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        data = {'nombre':"1", 'cantidad':"10", 'fecha_cad':"2018-20-20"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(PaqueteInventario.objects.count(), 0)

    def test_ac_21_7_Solo_permite_formato_de_fecha_en_campo_fecha(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        data = {'nombre':"1", 'cantidad':"10", 'fecha_cad':"Martes 10"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(PaqueteInventario.objects.count(), 0)

    def test_ac_21_8_Solo_permite_numeros_enteros_en_cantidad(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        data = {'nombre':"1", 'cantidad':"10.11", 'fecha_cad':"2019-12-12"}

        self.client.post(reverse('paquetes:agregar_inventario'), data)
        self.assertEqual(PaqueteInventario.objects.count(), 0)

    def test_ac_21_9_Se_agrega_exitosamente_el_paquete(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)
        paquete= Paquete.objects.first()
        #Obtener receta de la cual se compone el paquete
        receta = Receta.objects.first()
        receta_2=Receta.objects.last()

        #Verificar que existen 6 piezas disponibles en inventario de la receta 1 (la caduacada no la toma en cuenta)
        self.assertEqual(receta.obtener_cantidad_inventario(),6)

        # Verificar que existen 15 piezas disponibles en inventario de la receta 1 (la caduacada no la toma en cuenta)
        self.assertEqual(receta_2.obtener_cantidad_inventario(), 15)

        data = {'nombre':paquete.id, 'cantidad':"1", 'fecha_cad':"2019-12-10"}
        resp = self.client.post(reverse('paquetes:agregar_inventario'), data)

        # Verificar que se creó el paquete
        self.assertEqual(PaqueteInventario.objects.count(), 1)

        #Verificar que se actualiza la cantidad de piezas en inventario de las recetas
        self.assertEqual(receta.obtener_cantidad_inventario(), 1)
        self.assertEqual(receta_2.obtener_cantidad_inventario(), 5)

    def test_ac_21_10_No_se_agregan_paquetes_sin_inventario(self):
        self.assertEqual(PaqueteInventario.objects.count(), 0)

        data = {'nombre': "1", 'cantidad': "15", 'fecha_cad': "2019-12-10"}
        self.client.post(reverse('paquetes:agregar_inventario'), data)

        #Verificar que no se creó el paquete
        self.assertEqual(PaqueteInventario.objects.count(), 0)
#
class TestBorrarPaqueteCatalogo(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    def crear_paquete(self):
        return Paquete.objects.create(nombre="Paquete de Prueba", precio=12.0)

    def test_ac_26_1(self):
        self.assertEqual(Paquete.objects.count(), 0)
        p = self.crear_paquete()
        # data = {'nombre': "Paquete de Prueba", 'precio': 12}
        # self.client.post(reverse('paquetes:agregar_paquete'), data)
        self.assertEqual(Paquete.objects.count(), 1)

        # self.client.post(reverse('paquetes:borrar_paquete'), p.id)
        self.client.get(reverse('paquetes:borrar_paquete', kwargs={'id_paquete':p.id}))
        self.assertEqual(Paquete.objects.count(), 1)


    def test_ac_26_3(self):
        p = self.crear_paquete()
        self.client.get(reverse('paquetes:borrar_paquete', kwargs={'id_paquete':p.id}))
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(Paquete.objects.filter(deleted_at__isnull=True).count(), 0)



    def test_ac_26_2(self):
        p = self.crear_paquete()
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(len(resp.context['paquetes']),1)
        self.client.get(reverse('paquetes:borrar_paquete', kwargs={'id_paquete':p.id}))
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(len(resp.context['paquetes']),0)

#US24
class TestAgregarPaqueteCatalogo(TestCase):
    #Crear objetos de prueba
    def setUp(self):
        #Crear receta de prueba
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        Receta.objects.create(nombre="Receta de prueba", cantidad=100, duration=datetime.timedelta(days=1))

    def crear_Paquete(self):
        return Paquete.objects.create(nombre="Paquete de prueba", precio=10, estatus=1)

    def test_ac_24_1_agregar_paquete_lista_paquetes(self):
        #Post con información correcta
        data={'nombre': 'Rudy', 'precio': '1.50'}
        self.client.post(reverse('paquetes:agregar_paquete'), data)

        #Verificar que se creó el paquete
        self.assertEqual(Paquete.objects.count(), 1)

        #Verificar que aparece en la lista de paquetes
        resp = self.client.get(reverse('paquetes:lista_paquetes'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['paquetes']),1)
        self.assertEqual(resp.context['paquetes'][0].nombre, "Rudy")

    def test_ac_24_2_precio_incorrecto(self):
        #Post con precio 0
        data={'nombre':'Rudy', 'precio':0}
        resp = self.client.post(reverse('paquetes:agregar_paquete'),data)
        #Verificar que no se haya agregado
        self.assertEqual(Paquete.objects.count(),0)
        #Verificar mensaje de error
        self.assertFormError(resp, 'forma', 'precio', 'El precio del paquete debe ser mayor a 0.')

        #Post con precio negativo
        data={'nombre':'Edgar', 'precio':'-25.53'}
        resp = self.client.post(reverse('paquetes:agregar_paquete'),data)
        #Verificar que no se haya agregado
        self.assertEqual(Paquete.objects.count(),0)
        #Verificar mensaje de error
        self.assertFormError(resp, 'forma', 'precio', 'El precio del paquete debe ser mayor a 0.')

    def test_ac_24_3_paquete_mismo_nombre(self):
        paquete = self.crear_Paquete()

        #Intentar crear paquete con el mismo nombre
        data={'nombre':paquete.nombre, 'precio':100}
        resp = self.client.post(reverse('paquetes:agregar_paquete'), data)

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
        receta = Receta.objects.last()
        #Post correcto para agregar receta a un paquete
        data= {'receta':receta.id,'cantidad':'10','paquete':paquete.id}
        self.client.post(reverse('paquetes:agregar_receta_a_paquete'),data)

        #Verificar lista de paquetes
        resp=self.client.get(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        self.assertEqual(resp.status_code,200)
        self.assertContains(resp, '<td>Receta de prueba</td>')

    def test_ac_24_5_agregar_receta_repetida_a_paquete(self):
        #Crear paquete de prueba
        paquete = self.crear_Paquete()
        receta = Receta.objects.last()
        #Agregar receta a paquete
        RecetasPorPaquete.objects.create(receta=receta, paquete=paquete, cantidad=10)

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

        #Crear relación
        RecetasPorPaquete.objects.create(receta=receta, paquete=paquete, cantidad=10)

        #Verificar que ya no esté disponible
        resp = self.client.get(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        self.assertEqual(len(resp.context['recetas']),0)

    def test_ac_24_7_cantidad_receta_negativa(self):
        #Crear paquete para probar
        paquete = self.crear_Paquete()
        receta = Receta.objects.last()

        #Post con cantidad 0
        data= {'receta':receta.id,'cantidad':'0','paquete':paquete.id}
        self.client.post(reverse('paquetes:agregar_receta_a_paquete'),data)
        #Verificar que no se hizo la relación
        self.assertEqual(Paquete.objects.last().recetas.count(),0)

        #Post con cantidad negativa
        data= {'receta':receta.id,'cantidad':'-100','paquete':paquete.id}
        self.client.post(reverse('paquetes:agregar_receta_a_paquete'),data)

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
        receta.save()

        #Verificar que la receta no se muestra
        resp = self.client.get(reverse('paquetes:agregar_recetas_a_paquete', kwargs={'id_paquete':paquete.id}))
        self.assertEqual(len(resp.context['recetas']),0)


#US23
class TestEliminarPaquete(TestCase):
    #Inicializar base de datos
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        receta = Receta.objects.create(nombre="Receta de prueba 1", duration=datetime.timedelta(days=1))
        receta_2 = Receta.objects.create(nombre="Receta de prueba 2", duration=datetime.timedelta(days=1))
        # Receta 1 en inventario que caduca en 5 día
        RecetaInventario.objects.create(nombre=receta, cantidad=3,
                                        fecha_cad=datetime.datetime.now() + datetime.timedelta(days=5))
        # Receta 1 en inventario que caduca en 1 día
        RecetaInventario.objects.create(nombre=receta, cantidad=3,
                                        fecha_cad=datetime.datetime.now() + datetime.timedelta(days=5))
        # Receta 1 en inventario que ya caducó
        RecetaInventario.objects.create(nombre=receta, cantidad=3,
                                        fecha_cad=datetime.datetime.now() - datetime.timedelta(days=5))
        # Receta 2 en inventario
        RecetaInventario.objects.create(nombre=receta_2, cantidad=15,
                                        fecha_cad=datetime.datetime.now() + datetime.timedelta(days=10))

        paquete = Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta, cantidad=5)
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta_2, cantidad=10)

        # Agregar paquete inventario
        data = {'nombre': Paquete.objects.first().id, 'cantidad': "1", 'fecha_cad': "2019-12-10"}
        self.client.post(reverse('paquetes:agregar_inventario'), data)


    #Se actualiza cantidad disponible de paquetes
    def test_ac_23_1(self):
        resp = self.client.get(reverse('paquetes:lista_paquete_inventario'))
        self.assertEqual(resp.context['catalogo_paquetes'][0].total, 1)

        paquete_inventario = PaqueteInventario.objects.first()
        #borrar paquete
        self.client.get(reverse('paquetes:borrar_paquete_inventario', kwargs={'id_paquete_inventario':paquete_inventario.id}))

        #Verificar cantidad
        resp = self.client.get(reverse('paquetes:lista_paquete_inventario'))
        self.assertEqual(PaqueteInventario.objects.last().estatus, 0)

    #Se actualiza la cantidad de recetas disponibles
    def test_ac_23_2(self):
        #Verificar cantidad de recetas antes de borrar
        self.assertEqual(Receta.objects.first().obtener_cantidad_inventario(),1)
        self.assertEqual(Receta.objects.last().obtener_cantidad_inventario(),5)

        # borrar paquete
        paquete = PaqueteInventario.objects.last()
        resp = self.client.get(reverse('paquetes:borrar_paquete_inventario', kwargs={'id_paquete_inventario': paquete.id}))

        #Verificar la cantida de recetas después de borrar
        self.assertEqual(Receta.objects.first().obtener_cantidad_inventario(),6)
        self.assertEqual(Receta.objects.last().obtener_cantidad_inventario(),15)

        #Verificar que se borró el paquete
        self.assertEqual(PaqueteInventario.objects.last().estatus,0)

    #Solo un administrador logeado puede eliminar un paquete

# #US22
class TestEditarPaqueteInventario(TestCase):
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        receta = Receta.objects.create(nombre="Receta de prueba 1", duration=datetime.timedelta(days=1))
        receta_2 = Receta.objects.create(nombre="Receta de prueba 2", duration=datetime.timedelta(days=1))
        # Receta 1 en inventario que caduca en 5 día
        RecetaInventario.objects.create(nombre=receta, cantidad=10,
                                        fecha_cad=datetime.datetime.now() + datetime.timedelta(days=5))
        # Receta 1 en inventario que caduca en 1 día
        RecetaInventario.objects.create(nombre=receta, cantidad=10,
                                        fecha_cad=datetime.datetime.now() + datetime.timedelta(days=5))
        # Receta 1 en inventario que ya caducó
        RecetaInventario.objects.create(nombre=receta, cantidad=5,
                                        fecha_cad=datetime.datetime.now() - datetime.timedelta(days=5))
        # Receta 2 en inventario
        RecetaInventario.objects.create(nombre=receta_2, cantidad=40,
                                        fecha_cad=datetime.datetime.now() + datetime.timedelta(days=10))

        paquete = Paquete.objects.create(id=1, nombre="Paquete de prueba", precio=10, estatus=1)
        paquete.save()
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta, cantidad=5)
        RecetasPorPaquete.objects.create(paquete=paquete, receta=receta_2, cantidad=10)


        #Agregar un paquete de inventario
        data = {'nombre': paquete.id, 'cantidad': "2", 'fecha_cad': "2019-12-10"}
        resp = self.client.post(reverse('paquetes:agregar_inventario'), data)

        #Agregar una nueva receta en inventario, la cual tiene 0 ocupados.
        RecetaInventario.objects.create(nombre=receta_2, cantidad=10,
                                        fecha_cad=datetime.datetime.now() + datetime.timedelta(days=1))



    def test_ac_22_1_existencia_vista(self):
        respuesta = self.client.get(reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id}))
        self.assertEqual(respuesta.status_code, 200)

    def test_ac_22_2_El_objeto_se_actualiza_exitosamente(self):
        #La cantidad a editar es menor de la que había
        data = {'cantidad': "1",}
        resp = self.client.post(reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id}), data)
        # Las recetas de inventario que tienen no tienen ninguna  pieza ocupada no se alteran
        receta_sin_piezas_ocupadas = RecetaInventario.objects.last()
        self.assertEqual(receta_sin_piezas_ocupadas.ocupados,0)
        # Las cantidad de recetas en inventario se actualiza
        receta_1 = Receta.objects.first()
        self.assertEqual(receta_1.obtener_cantidad_inventario(), 15)

        receta_2 = Receta.objects.last()
        self.assertEqual(receta_2.obtener_cantidad_inventario(), 40)

        #Verificar que se cambió el número de paquetes inventario
        self.assertEqual(PaqueteInventario.objects.first().cantidad, 1)


        #La cantidad a editar es mayor a la que había y no existe suficiente en inventario
        data = {'cantidad': "50",}
        self.client.post((reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id})), data)

        #no se modificó nada
        self.assertEqual(receta_1.obtener_cantidad_inventario(), 15)
        self.assertEqual(receta_2.obtener_cantidad_inventario(), 40)
        self.assertEqual(PaqueteInventario.objects.first().cantidad, 1)

        #La cantidad a editar es mayor a la que había y sí existe suficiente en inventario
        data = {'cantidad': "2"}
        self.client.post(reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id}), data)
        #Se restan las recetas de inventario
        self.assertEqual(receta_1.obtener_cantidad_inventario(), 10)
        self.assertEqual(receta_2.obtener_cantidad_inventario(), 30)
        #La receta que se agregó al último ya tiene piezas ocupadas
        self.assertEqual(RecetaInventario.objects.filter(nombre=receta_2).last().cantidad, 10)

    def test_ac_22_6_test_ac_22_4_Existe_mensaje_de_error_al_dejar_la_cantidad_vacia(self):
        data = {'nombre':"1", 'fecha_cad':"2019-12-12"}
        resp = self.client.post(reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id}), data)
        self.assertFormError(resp, 'form', 'cantidad', "Debes seleccionar una cantidad mayor a 0.")

    def test_ac_22_7_Cantidad_no_puede_ser_negativo(self):
        data = {'nombre':"1", 'cantidad':"-12", 'fecha_cad':"2019-12-12"}
        resp = self.client.post(reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id}), data)
        update = PaqueteInventario.objects.first()
        self.assertNotEqual(update.cantidad, "-12")

    def test_ac_22_8_Mensaje_de_error_al_introducir_numero_negativo(self):
        data = {'nombre':"1", 'cantidad':"-12", 'fecha_cad':"2019-12-12"}
        resp = self.client.post(reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id}), data)
        self.assertFormError(resp, 'form', 'cantidad', "Debes seleccionar un número entero mayor a 0.")

    def test_ac_22_12_Campo_cantidad_sin_strings(self):
        data = {'nombre':"1", 'cantidad':"repollo", 'fecha_cad':"2019-12-12"}
        resp = self.client.post(reverse('paquetes:editar_paquete_inventario', kwargs={'id_paquete': PaqueteInventario.objects.first().id}), data)
        update = PaqueteInventario.objects.first()
        self.assertNotEqual(update.cantidad, "repollo")

class TestVerCostoProductoTerminado(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                            is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

        Paquete.objects.create(
            nombre="Paquete",
            precio="120",
        )
        PaqueteInventario.objects.create(
            id=1,
            nombre=Paquete.objects.all().first(),
            cantidad=1,
            ocupados=0,
            fecha_cad='2018-10-10',
            costo=20
        )

    def testVerCostoPaquete(self):
        resp = self.client.post('/paquetes/paquetes_por_catalogo/', {'id_paquete': 1})
        for paq in resp.context['detalle_paquetes_en_inventario']:
            self.assertEqual(20, paq.costo)