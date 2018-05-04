from django.test import TestCase
from django.urls import reverse
import datetime
from django.utils import timezone
from paquetes.models import PaqueteInventario, Paquete, RecetasPorPaquete
from recetas.models import Receta, RecetaInventario, RelacionRecetaMaterial
from materiales.models import Material, Unidad, MaterialInventario
from django.contrib.auth.models import User, Group
from mermas.models import MermaPaquete, MermaMaterial, MermaReceta


#Test case de la US 20
class TestListaMerma(TestCase):

     def setUp(self):
         Group.objects.create(name="admin")
         user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
         user.save()
         self.client.login(username='temporary', password='temporary')
         unidad = Unidad.objects.create(nombre="UnidadT", id=1)
         material = Material.objects.create(nombre="Buebito", codigo="123456789", unidad_entrada_id=1, unidad_maestra_id=1)
         materialinv = MaterialInventario.objects.create(
             material=material,
             unidad_entrada=unidad,
             cantidad=10,
             costo=120,
             fecha_cad="2059-03-03 12:31:06-05")
         recetacat = Receta.objects.create(
             nombre="RecetaT",
             cantidad=20,
             duration=datetime.timedelta(days=1),
             #material=material
             )
         relacion = RelacionRecetaMaterial.objects.create(
             receta=recetacat,
             material=material,
             cantidad=2)
         recetainv = RecetaInventario.objects.create(
             nombre=recetacat,
             cantidad=10,
             fecha_cad="2060-03-03 12:31:06-05")
         paquetecat = Paquete.objects.create(
             nombre="PaqueteT",
             #recetas=recetacat,
             precio=10)
         relacionrecpaq = RecetasPorPaquete.objects.create(
             paquete=paquetecat,
             receta=recetacat,
             cantidad=1)
         paqueteinv = PaqueteInventario.objects.create(
             nombre=paquetecat,
             cantidad=1,
             fecha_cad="2060-03-03 12:31:06-05")
         merma = MermaPaquete.objects.create(
             nombre=paqueteinv,
             cantidad=1,
             fecha="2018-03-03 12:31:06-05",
             descripcion="Se lo comio valter")
         merma2 = MermaMaterial.objects.create(
             nombre=materialinv,
             cantidad=1,
             fecha="2018-03-03 12:31:06-05",
             descripcion="Se lo comio valter")
         merma3 = MermaReceta.objects.create(
             nombre=recetainv,
             cantidad=1,
             fecha="2018-03-03 12:31:06-05",
             descripcion="Se lo comio valter")

     def test_ac1_existe_la_vista(self):
         resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
         self.assertEqual(resp.status_code, 200)

     def test_ac2_muestra_lista(self):
         resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(len(resp.context['mermas']), 1)

     def test_ac3_muestra_elementos_correctos(self):
         resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(len(resp.context['mermas']), 1)
         merm = MermaPaquete.objects.first()
         self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)
     #INICIA RECETAS
     def test_ac1_existe_la_vista_recetas(self):
         resp = self.client.get(reverse('mermas:lista_mermas_receta'))
         self.assertEqual(resp.status_code, 200)

     def test_ac2_muestra_lista_recetas(self):
         resp = self.client.get(reverse('mermas:lista_mermas_receta'))
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(len(resp.context['mermas']), 1)

     def test_ac3_muestra_elementos_correctos_recetas(self):
         resp = self.client.get(reverse('mermas:lista_mermas_receta'))
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(len(resp.context['mermas']), 1)
         merm = MermaReceta.objects.first()
         self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)
     #TERMINA RECETAS
     #INICIA MATERIA PRIMA
     def test_ac1_existe_la_vista_materiales(self):
         resp = self.client.get(reverse('mermas:lista_mermas_material'))
         self.assertEqual(resp.status_code, 200)

     def test_ac2_muestra_lista_materiales(self):
         resp = self.client.get(reverse('mermas:lista_mermas_material'))
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(len(resp.context['mermas']), 1)

     def test_ac3_muestra_elementos_correctos_materiales(self):
         resp = self.client.get(reverse('mermas:lista_mermas_material'))
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(len(resp.context['mermas']), 1)
         merm = MermaMaterial.objects.first()
         self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)
     #TERMINA MATERIA PRIMA


#Test case de la US20
class TestMermaMateria(TestCase):

    #Preparacion de ambiente de pruebas para las mermas
    def setUp(self):
        #Autenticar el login
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                        is_superuser='True')
        user.save()
        #Creación de objetos para pruebas
        self.client.login(username='temporary', password='temporary')
        unidad = Unidad.objects.create(nombre="UnidadT", id=1)
        material = Material.objects.create(nombre="Buebito", codigo="123456789", unidad_entrada_id=1, unidad_maestra_id=1)
        material.save()
        materialinv = MaterialInventario.objects.create(
            material=material,
            unidad_entrada=unidad,
            cantidad=10,
            costo=120,
            fecha_cad="2059-03-03 12:31:06-05")
        materialinv.save()
        recetacat = Receta.objects.create(
            nombre="RecetaT",
            cantidad=20,
            duration=datetime.timedelta(days=1),
            #material=material
            )
        relacion = RelacionRecetaMaterial.objects.create(
            receta=recetacat,
            material=material,
            cantidad=2)
        recetainv = RecetaInventario.objects.create(
            nombre=recetacat,
            cantidad=10,
            fecha_cad="2060-03-03 12:31:06-05")
        paquetecat = Paquete.objects.create(
            nombre="PaqueteT",
            #recetas=recetacat,
            precio=10)
        relacionrecpaq = RecetasPorPaquete.objects.create(
            paquete=paquetecat,
            receta=recetacat,
            cantidad=1)
        paqueteinv = PaqueteInventario.objects.create(
            nombre=paquetecat,
            cantidad=1,
            fecha_cad="2060-03-03 12:31:06-05")
        merma = MermaPaquete.objects.create(
            nombre=paqueteinv,
            cantidad=1,
            fecha="2018-03-03 12:31:06-05",
            descripcion="Se lo comio valter")
        merma2 = MermaMaterial.objects.create(
            nombre=materialinv,
            cantidad=1,
            fecha="2018-03-03 12:31:06-05",
            descripcion="Se lo comio valter")
        merma3 = MermaReceta.objects.create(
            nombre=recetainv,
            cantidad=1,
            fecha="2018-03-03 12:31:06-05",
            descripcion="Descripcion")

    #Revisión de que exista la vista
    def test_ac1_existe_la_vista(self):
        #Revisa que haya respuesta de la vista por parte del servidor
        resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
        self.assertEqual(resp.status_code, 200)

    #Revisión de que la lista se muestre
    def test_ac2_muestra_lista(self):
        #Revisión de que haya una respuesta de la vista por parte del servidor y que se muestre el objeto de forma correcta
        resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['mermas']), 1)

    #Revisión de que se muestren de forma correcta los elementos
    def test_ac3_muestra_elementos_correctos(self):
        #Revisión de que haya una respuesta de la vista por parte del servidor y que el objeto mostrado sea correcto
        resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['mermas']), 1)
        merm = MermaPaquete.objects.first()
        self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)


    #INICIA RECETAS
    def test_ac1_existe_la_vista_recetas(self):
        #Revisa que haya respuesta de la vista por parte del servidor
        resp = self.client.get(reverse('mermas:lista_mermas_receta'))
        self.assertEqual(resp.status_code, 200)

#Revisión de que la lista se muestre
    def test_ac2_muestra_lista_recetas(self):
        #Revisión de que haya una respuesta de la vista por parte del servidor y que se muestre el objeto de forma correcta
        resp = self.client.get(reverse('mermas:lista_mermas_receta'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['mermas']), 1)

    #Revisión de que se muestren de forma correcta los elementos
    def test_ac3_muestra_elementos_correctos_recetas(self):
        #Revisión de que haya una respuesta de la vista por parte del servidor y que el objeto mostrado sea correcto
        resp = self.client.get(reverse('mermas:lista_mermas_receta'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['mermas']), 1)
        merm = MermaReceta.objects.first()
        self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)
    #TERMINA RECETAS
    #INICIA MATERIA PRIMA
    def test_ac1_existe_la_vista_materiales(self):
        #Revisa que haya respuesta de la vista por parte del servidor
        resp = self.client.get(reverse('mermas:lista_mermas_material'))
        self.assertEqual(resp.status_code, 200)

    #Revisión de que la lista se muestre
    def test_ac2_muestra_lista_materiales(self):
        #Revisión de que haya una respuesta de la vista por parte del servidor y que se muestre el objeto de forma correcta
        resp = self.client.get(reverse('mermas:lista_mermas_material'))
        self.assertTrue(MermaMaterial.objects.first() in resp.context['mermas'])


    #Revisión de que se muestren de forma correcta los elementos


    #20.2 La merma no se puede dejar sin una descripción
    def test_no_se_deja_sin_descripcion(self):
        #Material del catálogo
        material_catalogo = Material.objects.first()

        #Material inventario inventario a mermar
        material_inventario = MaterialInventario.objects.first()

        #Contar mermas y material actual en inventario
        self.assertEqual(material_catalogo.obtener_cantidad_inventario_fisico(), 0)
        self.assertEqual(MermaPaquete.objects.count(), 1)

        #Preparar POST y enviar sin descripción
        data = {'nombre':material_inventario.id, 'fecha':'2018-04-07', 'cantidad':5}
        self.client.post(reverse('mermas:agregar_merma_materiales'), data)

        #La cantidad en inventario físico no se altera y tampoco se crea el objeto de merma
        self.assertEqual(material_catalogo.obtener_cantidad_inventario_fisico(), 0)
        self.assertEqual(MermaPaquete.objects.count(), 1)

    #20.7, 20.8, 20,9  Existe la vista de lista de mermas, muestra la lista con las mermas
    def test_existe_vista_lista_mermas_materia(self):
        #Verificar que existe la vista

        resp = self.client.get(reverse('mermas:lista_mermas_material'))
        self.assertEqual(resp.status_code,200)

        #Verificar que deuvlve la lista de mermas
        self.assertTrue('mermas' in resp.context)


class TestMermaReceta(TestCase):

    def setUp(self):
        # Verificar cantidad inicial
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                        is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

        # Crear Receta
        receta = Receta.objects.create(nombre="Receta de prueba", duration=timezone.timedelta(days=10))

        # Crear Receta Inventario
        RecetaInventario.objects.create(nombre=receta, cantidad=15,ocupados=0,
                                        fecha_cad=timezone.now() + timezone.timedelta(days=10))

    #20.1,20.3. Se puede ver la lista de mermas receta y se actualizan las cantidades cuando se realiza el ajuste
    def test_se_actualiza_cantidad_recetas(self):
        #Obtener receta del catálogo
        receta_catalogo = Receta.objects.first()

        #Verificar antidad inicial
        self.assertEqual(receta_catalogo.obtener_cantidad_inventario_con_caducados(), 15)
        self.assertEqual(MermaReceta.objects.count(),0)

        #Obtener receta inventario del catálogo
        receta_inventario = RecetaInventario.objects.first()

        #Preparar y hacer POST correcto
        data = {'nombre':receta_inventario.id, 'cantidad':-10, 'descripcion':"Las galletas se quemaron"}
        self.client.post(reverse('mermas:agregar_merma_recetas'),data)

        #Verificar cantidad y que se haya creado el objecto de meram
        self.assertEqual(receta_catalogo.obtener_cantidad_inventario_con_caducados(),5)
        self.assertEqual(MermaReceta.objects.count(),1)

    #20.2 El ajuste de inventario no se puede hacer sin una descripción
    def test_no_se_crea_sin_descripcion_merma_receta(self):
        #Verificar cantidad inicial
        self.assertEqual(MermaReceta.objects.count(),0)

        #Obtener receta inventario
        receta_inventario = RecetaInventario.objects.first()

        #Preparar y mandar POST sin descripción
        data = {'nombre':receta_inventario.id, 'cantidad':10, 'fecha':'2018-04-18', 'descripcion':''}
        self.client.post(reverse('mermas:agregar_merma_recetas'), data)

        #Verificar que no se creó la merma de la receta
        self.assertEqual(MermaReceta.objects.count(),0)

    #20.10,20.11,20.12 Se puede ver la lista de paquetes y muestra la lista de paquetes
    def test_la_vista_existe_y_muestra_vista_merma_receta(self):
        #Verificar que la vista existe
        resp = self.client.get(reverse('mermas:lista_mermas_receta'))
        self.assertEqual(resp.status_code,200)

        #Verificar que la lista se ve en la lista
        self.assertTrue('mermas' in resp.context)

class TestMermaPaquete(TestCase):

    def setUp(self):
        #Crear Usuario y logear
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                        is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

        #Crear Paquete en catálogo y en inventario
        paquete_catalogo = Paquete.objects.create(nombre="Paquete de prueba", precio="100")
        paquete_inventario = PaqueteInventario.objects.create(nombre=paquete_catalogo, cantidad=10, ocupados=0)

    #20.1,20.3,20.4,20.5, 20.6 Se puede hacer el ajuste de inventario y se muestra en la lista de ajuste de inventario de paquetes
    def test_ajuste_inventario_correcto(self):
        #Se obtiene el paquete en catálogo y el paquete en inventario
        paquete_catalogo = Paquete.objects.first()
        paquete_inventario = PaqueteInventario.objects.first()

        #Verificar cantidad inicial en inventario
        self.assertEqual(paquete_catalogo.obtener_inventario_fisico(), 10)
        self.assertEqual(MermaPaquete.objects.count(),0)

        #Se prepara el POST correcto y se manda
        data = {"nombre":paquete_inventario.id, "cantidad":-5, "descripcion":"Los paquetes se regalaron a los chicos del Tec."}
        self.client.post(reverse('mermas:agregar_merma_paquetes'),data)
        #Verificar que se actualiza la cantidad en inventario
        self.assertEqual(paquete_catalogo.obtener_inventario_fisico(), 5)
        self.assertEqual(MermaPaquete.objects.count(),1)

    #20.2
    def test_no_se_manda_sin_descripcion(self):
        #Se obtiene el paquete de catálogo y de inventario
        paquete_catalogo = Paquete.objects.first()
        paquete_inventario = PaqueteInventario.objects.first()

        #Se verifican las cantidades iniciales
        self.assertEqual(paquete_catalogo.obtener_inventario_fisico(),10)
        self.assertEqual(MermaPaquete.objects.count(),0)

        #Se prepara el POST sin descripción y se manda
        data = {'nombre':paquete_inventario.id, 'cantidad':10, 'fecha':'2018-04-18', 'descripcion':""}
        self.client.post(reverse('mermas:agregar_merma_paquetes'), data)

        #Verificar que no se completó la acción
        self.assertEqual(paquete_catalogo.obtener_inventario_fisico(),10)
        self.assertEqual(MermaPaquete.objects.count(),0)