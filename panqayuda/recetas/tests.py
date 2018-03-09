from django.test import TestCase
from materiales.models import Material
from recetas.models import Receta, RelacionRecetaMaterial
import datetime
from django.urls import reverse

#US27-Agregar Receta
class TestAgregarReceta(TestCase):

    def crear_receta_prueba(self):
        return Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    def crear_material_prueba(self):
        return Material.objects.create(nombre="Huevo", unidad="kg", codigo="T1")

    def crear_relacion_receta_material(self,receta,material):
        RelacionRecetaMaterial.objects.create(receta=receta, material=material, cantidad=10)


    #Verificar que la vista sea correctamente encontrada
    def test_vista_agregar_receta(self):
        resp = self.client.get(reverse('recetas:agregar_receta'))
        self.assertEqual(resp.status_code,200)

    #AC 27.1, 27.5, 27.7 La receta se puede ver en la lista de recetas una vez que se ha agregado, se agrega aunque
    #no se haya de terminado de agregar materiales, y puede tener cualquier caracter
    def test_ac_27_1(self):
        #Base de datos vacía
        self.assertEqual(Receta.objects.count(), 0)

        #Simular POST con información correcta
        data = {'nombre': "Receta de prueba", 'cantidad': 20, 'duration':'1 day'}
        self.client.post(reverse('recetas:agregar_receta'), data)

        #Verificar que se creó el objeto
        self.assertEqual(Receta.objects.count(), 1)

        #Verificar la lista de recetas
        resp = self.client.get(reverse('recetas:lista_de_recetas'))
        self.assertEqual(len(resp.context['recetas']), 1)
        self.assertEqual(resp.context['recetas'][0].nombre, "Receta de prueba")

        #Crear receta con caracteres especiales
        data = {'nombre': "Canción de náàvïda", 'cantidad': 20, 'duration': '1 day'}
        self.client.post(reverse('recetas:agregar_receta'), data)
        self.assertEqual(Receta.objects.count(), 2)

    #AC 27.2 Los materiales que ya están en la receta no aparecen disponibles para agregar
    def test_ac_27_2(self):
        #Crear objetos de prueba
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        #Asignar material a receta
        self.crear_relacion_receta_material(r,m)

        #Verificar que el material no se le muestra al usuario para agregar
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        self.assertEqual(len(resp.context['materiales_disponibles']),0)


    #AC 27.3 La cantidad de producto que genera la receta sólo puede ser un número positivo entero.
    def test_ac_27_3(self):
        #POST con cantidad negativa
        data = {'nombre': 'Receta de prueba', 'cantidad': '-5', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)

        #Verificar que no se haya creado
        self.assertEqual(Receta.objects.count(),0)

        #POST con cantidad decimal
        data = {'nombre': 'Receta de prueba', 'cantidad': '0.05', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)

        # Verificar que no se haya creado
        self.assertEqual(Receta.objects.count(), 0)

        #POST con cantidad entera positiva
        data = {'nombre': 'Receta de prueba', 'cantidad': '1', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)
        self.assertEqual(Receta.objects.count(), 1)

    #AC 27.4 No se puede agregar un material que ya esté en la receta
    def test_ac_27_4(self):
        #Asignar material a receta
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        self.crear_relacion_receta_material(r,m)
        #Verificar que se hizo la asignación
        self.assertEqual(r.material.count(), 1)

        #POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}), data)

        #Verificar que no se haya hecho la asignación
        self.assertEqual(r.material.count(), 1)

        #Verificar mensaje de error
        self.assertFormError(resp, 'form','material', "El material seleccionado ya está en la receta.")

    #AC 27.6 No se puede agregar una receta con un nombre existente
    def test_ac_27_6(self):
        #Crear receta de prueba con nombre 'Receta de prueba'
        r = self.crear_receta_prueba()
        # POST con nombre repetido
        data = {'nombre': 'receta de prueba', 'cantidad': '10', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:agregar_receta'), data)

        #Verificar que no se haya creado la receta
        self.assertEqual(Receta.objects.count(),1)

        #Verificar mensaje de error
        self.assertFormError(resp,'form','nombre',"Esta receta ya existe")

    #AC 27.8 Cuando se agrega un material con su respectiva cantidad a la receta, se agrega en la lista de materiales
    # de la receta
    def test_ac_27_8(self):
        # Asignar material a receta
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()

        # POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        # Verificar que está en la lista de materiales
        self.assertEqual(len(resp.context['materiales_actuales']), 1)
        self.assertEqual(resp.context['materiales_actuales'][0].material.nombre, m.nombre)

    #AC 27.9 Sólo un usuario administrtivo puede agregar una receta -- PENDIENTE

    #AC 27.10 Cuando se termina agregar la receta, el usuario visualiza un resumen de esta.
    def test_ac_27_10(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        #Verificar que el link que lleve a la vista de detalle se encuentre en la respuesta
        self.assertContains(resp, reverse('recetas:detallar_receta', kwargs={'id_receta':r.id}))
        #Verificar que la vista se muestra correctamente
        resp = self.client.get(reverse('recetas:detallar_receta', kwargs={'id_receta':r.id}))
        self.assertEquals(resp.status_code,200)

    #AC 27.11 Un material que se agrega a la receta no puede dejarse sin cantidad o cantidad 0.
    def test_ac_27_11(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        # POST con cantidad negativa
        data = {'material': m.nombre, 'cantidad': '-1', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)

        # POST con cantidad cero
        data = {'material': m.nombre, 'cantidad': '0', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)

        # POST sin cantidad
        data = {'material': 'Huevo', 'cantidad': '', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)
        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)
        # Verificar mensaje de error
        self.assertFormError(resp,'form','cantidad','Debes seleccionar una cantidad.')
        # POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que sí se hizo la relación
        self.assertEqual(r.material.count(), 1)
        self.assertEqual(r.material.first().status, 1)

    #AC 27.12 El nombre de la receta no puede estar vacío
    def ac_27_12(self):
        # Simular POST con información correcta
        data = {'nombre': "", 'cantidad': 20, 'duration': '1 day'}
        self.client.post(reverse('recetas:agregar_receta'), data)

        self.assertEqual(Receta.objects.count(),0)

    #AC 27.13 No se pueden agregan materiales a una receta inexistente
    def ac_27_13(self):
        #Verificar que una receta inexistente regrese 404
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_materiales':1750}))
        self.assertEqual(resp.status_code, 404)

        #Verificar que una receta que se haya dado de baja arroje error 404
        r = self.crear_receta_prueba()
        r.status = 0

        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_materiales':1}))
        self.assertEqual(resp.status_code, 404)


#US28-Editar Receta
class TestEditarReceta(TestCase):

    def crear_receta_prueba(self):
        return Receta.objects.create(nombre="Receta de prueba", cantidad=20, duration=datetime.timedelta(days=1))

    def crear_material_prueba(self):
        return Material.objects.create(nombre="Huevo", unidad="kg", codigo="T1")

    def crear_relacion_receta_material(self,receta,material):
        RelacionRecetaMaterial.objects.create(receta=receta, material=material, cantidad=10)

    #Verificar que la vista sea correctamente encontrada
    def test_vista_editar_receta(self):
        #Crear objetos de prueba
        r = self.crear_receta_prueba()

        resp = self.client.get(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}))
        self.assertEqual(resp.status_code,200)

    #Verificar que la receta editada se puede ver en la lista
    def test_ver_receta_editada_en_lista(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()
        
        #Base de datos vacía
        self.assertEqual(Receta.objects.count(), 0)

        #Simular POST con información correcta
        data = {'nombre': "Receta de prueba", 'cantidad': 20, 'duration':'1 day'}
        self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        #Verificar que se creó el objeto
        self.assertEqual(Receta.objects.count(), 1)

        #Verificar la lista de recetas
        resp = self.client.get(reverse('recetas:lista_de_recetas'))
        self.assertEqual(len(resp.context['recetas']), 1)
        self.assertEqual(resp.context['recetas'][0].nombre, "Receta de prueba")

        #Editar receta con caracteres especiales
        data = {'nombre': "Canción de náàvïda", 'cantidad': 20, 'duration': '1 day'}
        self.client.post(reverse('recetas:editar_receta'), data)
        self.assertEqual(Receta.objects.count(), 2)

    #Los materiales que ya están en la receta no aparecen disponibles para agregar
    def test_validar_materiales(self):
        #Crear objetos de prueba
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        #Asignar material a receta
        self.crear_relacion_receta_material(r,m)

        #Verificar que el material no se le muestra al usuario para agregar
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        self.assertEqual(len(resp.context['materiales_disponibles']),0)

    #La cantidad de producto que genera la receta sólo puede ser un número positivo entero.
    def test_cantidad_producto_positiva(self):
        #Crear objetos de prueba
        r = self.crear_receta_prueba()

        #POST con cantidad negativa
        data = {'nombre': 'Receta de prueba', 'cantidad': '-5', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        #Verificar que no se haya creado
        self.assertEqual(Receta.objects.count(),0)

        #POST con cantidad decimal
        data = {'nombre': 'Receta de prueba', 'cantidad': '0.05', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:editar_receta'), data)

        # Verificar que no se haya creado
        self.assertEqual(Receta.objects.count(), 0)

        #POST con cantidad entera positiva
        data = {'nombre': 'Receta de prueba', 'cantidad': '1', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:editar_receta'), data)
        self.assertEqual(Receta.objects.count(), 1)

    #No se puede agregar un material que ya esté en la receta
    def test_material_existente(self):
        #Asignar material a receta
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        self.crear_relacion_receta_material(r,m)
        #Verificar que se hizo la asignación
        self.assertEqual(r.material.count(), 1)

        #POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta':r.id}), data)

        #Verificar que no se haya hecho la asignación
        self.assertEqual(r.material.count(), 1)

        #Verificar mensaje de error
        self.assertFormError(resp, 'form','material', "El material seleccionado ya está en la receta.")

    #No se puede agregar una receta con un nombre existente
    def test_receta_nombre_existente(self):
        #Crear receta de prueba con nombre 'Receta de prueba'
        r = self.crear_receta_prueba()
        # POST con nombre repetido
        data = {'nombre': 'receta de prueba', 'cantidad': '10', 'duration': '1 days'}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        #Verificar que no se haya creado la receta
        self.assertEqual(Receta.objects.count(),1)

        #Verificar mensaje de error
        self.assertFormError(resp,'form','nombre',"Esta receta ya existe")

    #Cuando se agrega un material con su respectiva cantidad a la receta, se agrega en la lista de materiales
    # de la receta
    def test_agregar_material(self):
        # Asignar material a receta
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()

        # POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        resp = self.client.get(reverse('recetas:editar_receta', kwargs={'id_receta':r.id}))
        # Verificar que está en la lista de materiales
        #self.assertEqual(len(resp.context['materiales_actuales']), 1)
        #self.assertEqual(resp.context['materiales_actuales'][0].material.nombre, m.nombre)

    #Cuando se termina agregar la receta, el usuario visualiza un resumen de esta.
    def test_resumen_receta(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta':r.id}))
        #Verificar que el link que lleve a la vista de detalle se encuentre en la respuesta
        self.assertContains(resp, reverse('recetas:detallar_receta', kwargs={'id_receta':r.id}))
        #Verificar que la vista se muestra correctamente
        resp = self.client.get(reverse('recetas:detallar_receta', kwargs={'id_receta':r.id}))
        self.assertEquals(resp.status_code,200)

    #Un material que se agrega a la receta no puede dejarse sin cantidad o cantidad 0.
    def test_cantidad_material(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()
        m = self.crear_material_prueba()
        # POST con cantidad negativa
        data = {'material': m.nombre, 'cantidad': '-1', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)

        # POST con cantidad cero
        data = {'material': m.nombre, 'cantidad': '0', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)

        # POST sin cantidad
        data = {'material': 'Huevo', 'cantidad': '', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)
        # Verificar que no se hizo la relación
        self.assertEqual(r.material.count(), 0)
        # Verificar mensaje de error
        self.assertFormError(resp,'form','cantidad','Debes seleccionar una cantidad.')
        # POST con cantidad correcta
        data = {'material': m.nombre, 'cantidad': '10', 'receta':r.id}
        resp = self.client.post(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}), data)

        # Verificar que sí se hizo la relación
        self.assertEqual(r.material.count(), 1)
        self.assertEqual(r.material.first().status, 1)

    #El nombre de la receta no puede estar vacío
    def test_nombre_vacio(self):
        # Crear objetos de prueba
        r = self.crear_receta_prueba()

        # Simular POST con información correcta
        data = {'nombre': "", 'cantidad': 20, 'duration': '1 day'}
        self.client.post(reverse('recetas:editar_receta', kwargs={'id_receta': r.id}), data)

        self.assertEqual(Receta.objects.count(),0)

    #No se pueden agregan materiales a una receta inexistente
    def test_material_receta_inexistente(self):
        #Verificar que una receta que se haya dado de baja arroje error 404
        r = self.crear_receta_prueba()
        r.status = 0

        #Verificar que una receta inexistente regrese 404
        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_receta': r.id}))
        self.assertEqual(resp.status_code, 404)



        resp = self.client.get(reverse('recetas:agregar_materiales', kwargs={'id_materiales':1}))
        self.assertEqual(resp.status_code, 404)

# ------------------------------ US 29 Borrar Receta ------------------------------ #


class TestBorrarReceta(TestCase):

    def crear_receta(self):
        return Receta.objects.create(nombre="Prueba de Bolillo", cantidad=12, duration=datetime.timedelta(days=1))

    def test_ac_29_1(self):
        self.assertEqual(Receta.objects.count(), 0)
        r = self.crear_receta()
        self.assertEqual(Receta.objects.count(), 1)
        self.client.get(reverse('recetas:borrar_receta', kwargs={'id_receta':r.id}))
        self.assertEqual(Receta.objects.count(), 1)


    def test_ac_29_2(self):
        r = self.crear_receta()
        resp = self.client.get(reverse('recetas:lista_de_recetas'))
        self.assertEqual(len(resp.context['recetas']),1)
        self.client.get(reverse('recetas:borrar_receta', kwargs={'id_receta':r.id}))
        resp = self.client.get(reverse('recetas:lista_de_recetas'))
        self.assertEqual(len(resp.context['recetas']),0)


    def test_ac_29_3(self):
        r = self.crear_receta()
        self.client.get(reverse('recetas:borrar_receta', kwargs={'id_receta':r.id}))
        self.assertEqual(Receta.objects.filter(deleted_at__isnull=True).count(), 0)
