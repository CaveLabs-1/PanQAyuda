from django.test import TestCase
from django.urls import reverse
from mermas.models import MermaPaquete, MermaMaterial, MermaReceta
import datetime
from django.utils import timezone
from paquetes.models import PaqueteInventario, Paquete, RecetasPorPaquete
from recetas.models import Receta, RecetaInventario, RelacionRecetaMaterial
from materiales.models import Material, Unidad, MaterialInventario
from django.contrib.auth.models import User, Group


#Test case de la US 20
# class TestListaMerma(TestCase):
#
#     def setUp(self):
#         Group.objects.create(name="admin")
#         user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
#         user.save()
#         self.client.login(username='temporary', password='temporary')
#         unidad = Unidad.objects.create(nombre="UnidadT")
#         material = Material.objects.create(nombre="Buebito", codigo=122212)
#         materialinv = MaterialInventario.objects.create(
#             material=material,
#             unidad_entrada=unidad,
#             cantidad=10,
#             cantidad_salida=10,
#             costo=120,
#             fecha_cad="2059-03-03 12:31:06-05")
#         recetacat = Receta.objects.create(
#             nombre="RecetaT",
#             cantidad=20,
#             duration=datetime.timedelta(days=1),
#             #material=material
#             )
#         relacion = RelacionRecetaMaterial.objects.create(
#             receta=recetacat,
#             material=material,
#             cantidad=2)
#         recetainv = RecetaInventario.objects.create(
#             nombre=recetacat,
#             cantidad=10,
#             fecha_cad="2060-03-03 12:31:06-05")
#         paquetecat = Paquete.objects.create(
#             nombre="PaqueteT",
#             #recetas=recetacat,
#             precio=10)
#         relacionrecpaq = RecetasPorPaquete.objects.create(
#             paquete=paquetecat,
#             receta=recetacat,
#             cantidad=1)
#         paqueteinv = PaqueteInventario.objects.create(
#             nombre=paquetecat,
#             cantidad=1,
#             fecha_cad="2060-03-03 12:31:06-05")
#         merma = MermaPaquete.objects.create(
#             nombre=paqueteinv,
#             cantidad=1,
#             fecha="2018-03-03 12:31:06-05",
#             descripcion="Se lo comio valter")
#         merma2 = MermaMaterial.objects.create(
#             nombre=materialinv,
#             cantidad=1,
#             fecha="2018-03-03 12:31:06-05",
#             descripcion="Se lo comio valter")
#         merma3 = MermaReceta.objects.create(
#             nombre=recetainv,
#             cantidad=1,
#             fecha="2018-03-03 12:31:06-05",
#             descripcion="Se lo comio valter")
#
#     def test_ac1_existe_la_vista(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
#         self.assertEqual(resp.status_code, 200)
#
#     def test_ac2_muestra_lista(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.context['mermas']), 1)
#
#     def test_ac3_muestra_elementos_correctos(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_paquete'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.context['mermas']), 1)
#         merm = MermaPaquete.objects.first()
#         self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)
#     #INICIA RECETAS
#     def test_ac1_existe_la_vista_recetas(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_receta'))
#         self.assertEqual(resp.status_code, 200)
#
#     def test_ac2_muestra_lista_recetas(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_receta'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.context['mermas']), 1)
#
#     def test_ac3_muestra_elementos_correctos_recetas(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_receta'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.context['mermas']), 1)
#         merm = MermaReceta.objects.first()
#         self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)
#     #TERMINA RECETAS
#     #INICIA MATERIA PRIMA
#     def test_ac1_existe_la_vista_materiales(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_material'))
#         self.assertEqual(resp.status_code, 200)
#
#     def test_ac2_muestra_lista_materiales(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_material'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.context['mermas']), 1)
#
#     def test_ac3_muestra_elementos_correctos_materiales(self):
#         resp = self.client.get(reverse('mermas:lista_mermas_material'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.context['mermas']), 1)
#         merm = MermaMaterial.objects.first()
#         self.assertEqual(resp.context['mermas'][0].descripcion, merm.descripcion)
#     #TERMINA MATERIA PRIMA


#Test case de la US20
class TestMermaMateria(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                        is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        #Crear Materia Prima
        m = Material.objects.create(nombre="Harina", codigo="H1")

        #Crear unidad
        u = Unidad.objects.create(nombre="kg")

        #Crear inventario de materia prima
        MaterialInventario.objects.create(material = m, unidad_entrada = u, cantidad=5, cantidad_disponible=20,porciones=15, costo=500, fecha_cad=timezone.now())
    #20.1, 20.3 El inventario de la materia se actualiza después de hacer la merma con datos correctos
    def test_merma_material_se_actualiza(self):
        # Material del catálogo
        material_catalogo = Material.objects.first()

        # Material inventario inventario a mermar
        material_inventario = PaqueteInventario.objects.first()

        # Contar mermas y material actual en inventario
        self.assertEqual(material_catalogo.obtener_cantidad_inventario_fisico(), 15)
        self.assertEqual(MermaMaterial.object.count(), 0)

        # Preparar POST correcto y enviar
        data = {'nombre': material_inventario.id, 'fecha': timezone.now(), 'cantidad': 5, 'descripcion': 'Le salieron unos hongos a la harina.'}
        self.client.post(reverse('mermas:agregar_merma_materiales'), data)

        #Verificar que se actualiza la cantidad en inventario y se crea el objeto de merma
        self.assertEqual(material_catalogo.obtener_cantidad_inventario_fisico(), 10)
        self.assertEqual(MermaPaquete.objects.count(),1)

        #Se ve la merma recién creada en la lista de mermas de materia prima
        resp = self.client.get(reverse('mermas:lista_mermas_material'))
        self.assertTrue(MermaMaterial.objects.first in resp.context['mermas'])

    #20.2 La merma no se puede dejar sin una descripción
    def test_no_se_deja_sin_descripcion(self):
        #Material del catálogo
        material_catalogo = Material.objects.first()

        #Material inventario inventario a mermar
        material_inventario = PaqueteInventario.objects.first()

        #Contar mermas y material actual en inventario
        self.assertEqual(material_catalogo.obtener_cantidad_inventario_fisico(), 15)
        self.assertEqual(MermaPaquete.object.count(), 0)

        #Preparar POST y enviar sin descripción
        data = {'nombre':material_inventario.id, 'fecha':timezone.now(), 'cantidad':5, 'descripcion':''}
        self.client.post(reverse('mermas:agregar_merma_materiales'), data)

        #La cantidad en inventario físico no se altera y tampoco se crea el objeto de merma
        self.assertEqual(material_catalogo.obtener_cantidad_inventario_fisico(), 15)
        self.assertEqual(MermaPaquete.object.count(),0)

    #20.7, 20.8, 20,9  Existe la vista de lista de mermas, muestra la lista con las mermas
    def test_existe_vista_lista_mermas_materia(self):
        #Verificar que existe la vista
        resp = self.client.get(reverse('mermas:lista_mermas_material'))
        self.assertEqual(resp.status_code,200)

        #Verificar que deuvlve la lista de mermas
        self.assertTrue('mermas' in resp.context)








