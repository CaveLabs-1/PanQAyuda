from django.test import TestCase
from django.urls import reverse
from .models import MermaPaquete, MermaMaterial, MermaReceta
import datetime
from django.utils import timezone
from paquetes.models import PaqueteInventario, Paquete, RecetasPorPaquete
from recetas.models import Receta, RecetaInventario, RelacionRecetaMaterial
from materiales.models import Material, Unidad, MaterialInventario
from django.contrib.auth.models import User, Group


#Test case de la US 20
class TestListaMerma(TestCase):

    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        unidad = Unidad.objects.create(nombre="UnidadT")
        material = Material.objects.create(nombre="Buebito", codigo=122212)
        materialinv = MaterialInventario.objects.create(
            material=material,
            unidad_entrada=unidad,
            cantidad=10,
            cantidad_salida=10,
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
# Create your tests here.
