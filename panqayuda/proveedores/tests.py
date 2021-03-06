from django.test import TestCase
from django.urls import reverse
from proveedores.models import Proveedor
from django.contrib.auth.models import User, Group
from django.shortcuts import render

#Test agregar proveedor
class TestAgregarProveedor(TestCase):

    def setUp(self):
        #Este set up crea un usuario, lo guarda e inicia sesion para que pueda comenzar los tests
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    #Revisar que la sesión exista
    def test_valid_session(self):
        session = self.client.session


    #Checa si existe la vista (template) para agregar el proveedor
    def test_existe_vista(self):
        #recupera el url de agregar_proveedor y guarda el resultado en la variable rest
        resp = self.client.get(reverse('proveedores:agregar_proveedor'))
        #Se utiliza la variable resp y se checa el codigo de respuesta si es exitoso
        self.assertEqual(resp.status_code, 200)

    #Checa si existe un objeto anteriormente, despues le manda una forma con informacion valida y checa si se guardó
    def test_ac1_el_proveedor_se_agrega_exitosamente(self):
        #Se checa si existe un proveedor previamente
        self.assertEqual(Proveedor.objects.count(), 0)
        #Se crea la informacion que se guardara al crear un proveedor
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        #Se crea un proveedor mandando una peticion POST al url de agregar_proveedor mandando el data
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        #Checa si se creo el proveedor
        self.assertEqual(Proveedor.objects.count(), 1)

    #checa que el nombre no este vacio
    def test_ac2_nombre_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        #Se guarda informacion erronea en la que falta el campo de nombre
        data = {'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        #Se checa que no se haya creado el proveedor con la informacion erronea
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el telefono tenga formato correcto
    def test_ac3_formato_telefono(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        #Se manda informacion erronea en la que el formato de telefono no cumple con los estandares de un numero normal
        data = {'nombre':"Bancomer", 'telefono':4155, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        #Se checa que no exista el proveedor con la informacion incorrecta
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el telefono no este vacio
    def test_ac4_telefono_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        #Se manda informacion erronea en la que el campo de telefono es inexistente
        data = {'nombre':"Bancomer", 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        #Se checa que no se haya creado el proveedor con la informacion erronea
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que la direccion no este vacia
    def test_ac5_direccion_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        #Se manda informacion erronea en la que el campo de direccion es erroneo
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        #Se checa que el proveedor no se haya creado con la informacion incorrecta
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el rfc no este vacio
    def test_ac6_rfc_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        #Se manda informacion erronea en la que no acepta un proveedor con el rfc vacio
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        #No se debe de guardar el proveedor con la informacion incorrecta
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que la razon social no este vacia
    def test_ac7_razon_social_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        #se manda informacion incorrecta en la que la razon social esta ausente
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        #No se debe de crear el objeto proveedor
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el email tenga el formato
    def test_ac8_email_no_valido(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemploarroba" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el email no este vacio
    def test_ac9_email_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)

    #retorno de error al dejar campo nombre vacio
    def test_ac10_retorno_error_campo_nombre_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)
        self.assertFormError(resp, 'form', 'nombre', "Debes introducir un nombre.")

    #retorno de error al dejar campo telefono vacio
    def test_ac11_retorno_error_campo_telefono_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)
        self.assertFormError(resp, 'form', 'telefono', "Debes introducir un telefono.")

    #retorno de error al dejar campo direccion vacio
    def test_ac12_retorno_error_campo_direccion_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)
        self.assertFormError(resp, 'form', 'direccion', "Debes poner una direccion.")

    #retorno error al dejar rfc vacio
    def test_ac13_retorno_error_campo_rfc_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)
        self.assertFormError(resp, 'form', 'rfc', "Debes poner un RFC.")

    #retorno de error al dejar razon social vacio
    def test_ac14_retorno_error_campo_razon_social_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)
        self.assertFormError(resp, 'form', 'razon_social', "Debes introducir razon social.")

    #retorno de error al dejar email vacio
    def test_ac15_retorno_error_campo_email_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks" }
        resp = self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)
        self.assertFormError(resp, 'form', 'email', "Debes poner un email.")

class TestListaProveedores(TestCase):
    #se cheva si la ruta para la vista existe
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_existe_la_vista(self):
        Proveedor.objects.create(nombre="Bancomer", telefono=4151043944, direccion="calle 100 corazones", rfc=45321343, razon_social="Somos unos cracks", email="ejemplo@hotmail.com")
        self.assertEqual(Proveedor.objects.count(), 1)
        resp = self.client.get(reverse('proveedores:lista_proveedores'))
        self.assertEqual(resp.status_code, 200)

    #Si no existe un proveedor regresa un 404
    def test_sin_proveedor_404(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        resp = self.client.get(reverse('proveedores:lista_proveedores'))
        self.assertEqual(resp.context['proveedores'].count(), 0)




class TestEliminarProveedor(TestCase):

    #Generación para el ambiente de pruebas de eliminar proveedor
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        proveedor = Proveedor.objects.create(
            nombre='Juan',
            telefono=12345678,
            direccion='el tec',
            rfc='holirfc',
            razon_social='eltecholi',
            email='v@v.com'
        )
        proveedor.save()

    #Test para borrar proveedores
    def test_borrar_proveedor(self):
        self.assertEqual(Proveedor.objects.count(), 1)
        #Se obtiene el objeto proveedor
        objetos = Proveedor.objects.first()
        #Se utiliza la view eliminar_proveedor
        self.client.get(reverse('proveedores:eliminar_proveedor', kwargs={'id_proveedor':objetos.id}))
        #Se valida que no haya objetos Proveedor que tenga vacío el campio deleted_at
        self.assertEqual(Proveedor.objects.filter(deleted_at__isnull=True).count(), 0)
# Create your tests here.

#Test US 2 Editar Proveedor
class TestEditarProveedor(TestCase):
    # Generación para el ambiente de pruebas de eliminar proveedor
    def setUp(self):
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary',
                                        is_superuser='True')
        user.save()
        self.client.login(username='temporary', password='temporary')
        proveedor = Proveedor.objects.create(
            nombre='Juan',
            telefono=12345678,
            direccion='el tec',
            rfc='holirfc',
            razon_social='eltecholi',
            email='prueba@prueba.com'
        )
        proveedor.save()

    def test_ac_1_no_editar_si_nombre_esta_vacio(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'',
            'telefono':'4424708341',
            'email':'prueba@hotmail.com',
            'direccion':'panqayuda',
            'rfc':'ASD123DSA1234',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)

    def test_ac_2_no_editar_si_telfeono_esta_vacio(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'',
            'email':'prueba@hotmail.com',
            'direccion':'panqayuda',
            'rfc':'ASD123DSA1234',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)

    def test_ac_2_no_editar_si_telfeono_no_es_valido(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'442470834asd',
            'email':'prueba@hotmail.com',
            'direccion':'panqayuda',
            'rfc':'ASD123DSA1234',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)


    def test_ac_3_no_editar_si_direccion_esta_valido(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'4424708341',
            'email':'prueba@hotmail.com',
            'direccion':'',
            'rfc':'ASD123DSA1234',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)

    def test_ac_4_no_editar_si_rfc_esta_vacio(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'4424708341',
            'email':'prueba@hotmail.com',
            'direccion':'calle pan que ayuda',
            'rfc':'',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)

    def test_ac_5_no_editar_si_email_esta_vacio(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'4424708341',
            'email':'',
            'direccion':'calle pan que ayuda',
            'rfc':'ASD123DSA1234',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)

    def test_ac_5_no_editar_si_email_no_es_valido(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'4424708341',
            'email':'unemailnovalido.com',
            'direccion':'calle pan que ayuda',
            'rfc':'ASD123DSA1234',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)


    def test_ac_6_no_editar_si_razonSocial_esta_vacio(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'4424708341',
            'email':'prueba@gmail.com',
            'direccion':'calle pan que ayuda',
            'rfc':'ASD123DSA1234',
            'razon_social':'',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertEqual(proveedor1.email, Proveedor.objects.get(id=proveedor1.id).email)

    def test_ac_7_editar_si_todoe_esta_correcto(self):
        proveedor1 = Proveedor.objects.all().first()

        # Datos del editar sin nombre pero lo demas bien
        data = {
            'nombre':'Alejandro',
            'telefono':'4424708341',
            'email':'prueba@gmail.com',
            'direccion':'calle pan que ayuda',
            'rfc':'ASD123DSA1234',
            'razon_social':'Pan Que Ayuda',
        }

        # Checar que el objecto antes de intetento de cambio es igual al de la base de datos
        resp = self.client.post(reverse('proveedores:editar_proveedor', kwargs={'id_proveedor': proveedor1.id}), data)
        proveedor2 = Proveedor.objects.all().first()
        self.assertFalse(proveedor1.email == Proveedor.objects.get(id=proveedor1.id).email)
        self.assertEqual(data['email'], Proveedor.objects.get(id=proveedor1.id).email)














