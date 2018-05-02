from django.test import TestCase
from django.urls import reverse
import datetime
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response
from django.template import RequestContext

#Test crear_usuario (US 48)
class TestCrearUsuario(TestCase):

    def setUp(self):
        #El setup sirve para crear un usuario en la base de datos, pero no inicia sesion
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        #Guarda el usuario que se creó
        user.save()

    #Solo un administrador puede crear un usuario
    def test_ac48_1_Solo_un_admin_crea_usuario(self):
        #Cuanto que solo exista el usuario que se creo en el setup
        self.assertEqual(User.objects.count(), 1)
        data = { 'password':"test", 'first_name':"Test", 'last_name':"Testerino", 'username':"Admond", 'email':"test@test.com", 'is_superuser':'True', 'is_staff':'True' }
        self.client.post(reverse('usuarios:lista_usuarios'), data)
        #Trato de crear un usuario pero como no esta iniciada la sesion entonces no se debe de crear
        self.assertEqual(User.objects.count(), 1)

    #Cuando creo un usuario, me aparece en la lista de usuarios
    def test_ac48_2_Se_muestra_en_lista_el_usuario(self):
        #Inicio de sesion
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #Checo que se imprima el usuario que ya existe desde el setup en la vista
        self.assertEqual(len(resp.context['usuarios']), 1)
        #Se crea un usuario pero ahora con la sesion iniciada
        data = { 'password':"test", 'first_name':"Test", 'last_name':"Testerino", 'username':"Admond", 'email':"test@test.com", 'is_superuser':'True', 'is_staff':'True' }
        self.client.post(reverse('usuarios:lista_usuarios'), data)
        #Se checa que se haya creado el usuario
        self.assertEqual(User.objects.count(), 2)
        #Se guarda la respuesta del servidor en resp2
        resp2 = self.client.get(reverse('usuarios:lista_usuarios'))
        #Estatus exitoso
        self.assertEqual(resp2.status_code, 200)
        #Se muestra en la lista correctamente
        self.assertEqual(len(resp2.context['usuarios']), 2)

    #Cuando se crea un usuario, este puede acceder al sistema con su usuario y contraseña
    def test_ac48_3_se_puede_acceder_al_sistema_con_el_usuario(self):
        #Inicio de sesion
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #Checo que se imprima el usuario que ya existe desde el setup en la vista
        self.assertEqual(len(resp.context['usuarios']), 1)
        #Se crea un usuario pero ahora con la sesion iniciada
        data = { 'password':"test", 'first_name':"Test", 'last_name':"Testerino", 'username':"Admond", 'email':"test@test.com", 'is_superuser':'True', 'is_staff':'True' }
        self.client.post(reverse('usuarios:lista_usuarios'), data)
        #Se checa que se haya creado el usuario
        self.assertEqual(User.objects.count(), 2)
        #Se guarda la respuesta del servidor en resp2
        resp2 = self.client.get(reverse('usuarios:lista_usuarios'))
        #Estatus exitoso
        self.assertEqual(resp2.status_code, 200)
        #Se muestra en la lista correctamente
        self.assertEqual(len(resp2.context['usuarios']), 2)
        #cerrar sesion
        resp3 = self.client.get("/logout")
        self.assertEqual(resp3.status_code, 301)
        #Se crea la informacion del usuario que se va a mandar
        data = {'username':"Admond", 'password':"test"}
        loginresp = self.client.post("/login", data)
        #Inicio de sesion exitoso
        self.assertEqual(loginresp.status_code, 301)

    #No puede haber usuarios sin contraseña
    def test_ac48_4_no_guarda_usuario_sin_pass(self):
        #Inicio de sesion
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #Checo que se imprima el usuario que ya existe desde el setup en la vista
        self.assertEqual(len(resp.context['usuarios']), 1)
        #Se manda informacion erronea en la que no tiene contraseña el usuario
        data = { 'first_name':"Test", 'last_name':"Testerino", 'username':"Admond", 'email':"test@test.com", 'is_superuser':'True', 'is_staff':'True' }
        self.client.post(reverse('usuarios:lista_usuarios'), data)
        #Se checa que se haya no se haya creado el usuario sin contraseña
        self.assertEqual(User.objects.count(), 1)

    #No puede haber usuarios sin nombre de usuaro
    def test_ac48_5_No_hay_usuario_sin_nombre(self):
        #Inicio de sesion
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #Checo que se imprima el usuario que ya existe desde el setup en la vista
        self.assertEqual(len(resp.context['usuarios']), 1)
        #Se manda informacion erronea en la que no tiene nombre el usuario
        data = { 'password':"test", 'first_name':"Test", 'last_name':"Testerino", 'email':"test@test.com", 'is_superuser':'True', 'is_staff':'True' }
        self.client.post(reverse('usuarios:lista_usuarios'), data)
        #Se checa que se haya no se haya creado el usuario sin contraseña
        self.assertEqual(User.objects.count(), 1)

#Tests caso de uso 50
class TestEliminarUsuario(TestCase):

    def setUp(self):
        #El setup sirve para crear un usuario en la base de datos, pero no inicia sesion
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        #Guarda el usuario que se creó
        user.save()

    #Cuando elimino a un usuario, ya no puede acceder al sistema con sus datos
    def test_ac50_1_al_eliminar_no_puedes_acceder(self):
        #Inicio de sesion
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #Checo que se imprima el usuario que ya existe desde el setup en la vista
        self.assertEqual(len(resp.context['usuarios']), 1)
        #Se crea un usuario pero ahora con la sesion iniciada
        data = { 'password':"test", 'first_name':"Test", 'last_name':"Testerino", 'username':"Admond", 'email':"test@test.com", 'is_superuser':'True', 'is_staff':'True' }
        self.client.post(reverse('usuarios:lista_usuarios'), data)
        #Se checa que se haya creado el usuario
        self.assertEqual(User.objects.count(), 2)
        #Se guarda la respuesta del servidor en resp2
        resp2 = self.client.get(reverse('usuarios:lista_usuarios'))
        #Estatus exitoso
        self.assertEqual(resp2.status_code, 200)
        #Se muestra en la lista correctamente
        self.assertEqual(len(resp2.context['usuarios']), 2)
        #cerrar sesion
        resp3 = self.client.get("/logout")
        self.assertEqual(resp3.status_code, 301)
        #Se crea la informacion del usuario que se va a mandar
        data = {'username':"Admond", 'password':"test"}
        loginresp = self.client.post("/login", data)
        #Inicio de sesion exitoso
        self.assertEqual(loginresp.status_code, 301)
        deleted_user = User.objects.get(username="temporary")
        #Usando el deleted_user se borra ese usuario con su id
        self.client.post(reverse('usuarios:borrar_usuario', kwargs={'id_usuario':deleted_user.id}))
        obj = User.objects.filter(is_active=1)
        #See checa que el estatus del usuario que queda sea de activo
        self.assertEqual(obj[0].username, 'Admond')
        self.client.get("/logout")
        data = {'username':"temporary", 'password':"temporary"}
        loginresp = self.client.post("/login", data)
        self.assertEqual(loginresp.status_code, 200)

    def test_ac50_2_Eliminados_no_salen_en_lista(self):
        #Inicio de sesion
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #Checo que se imprima el usuario que ya existe desde el setup en la vista
        self.assertEqual(len(resp.context['usuarios']), 1)
        #Se crea un usuario pero ahora con la sesion iniciada
        data = { 'password':"test", 'first_name':"Test", 'last_name':"Testerino", 'username':"Admond", 'email':"test@test.com", 'is_superuser':'True', 'is_staff':'True' }
        self.client.post(reverse('usuarios:lista_usuarios'), data)
        #Se checa que se haya creado el usuario
        self.assertEqual(User.objects.count(), 2)
        #Se guarda la respuesta del servidor en resp2
        resp2 = self.client.get(reverse('usuarios:lista_usuarios'))
        #Estatus exitoso
        self.assertEqual(resp2.status_code, 200)
        #Se muestra en la lista correctamente
        self.assertEqual(len(resp2.context['usuarios']), 2)
        deleted_user = User.objects.get(username="Admond")
        #Usando el deleted_user se borra ese usuario con su id
        self.client.post(reverse('usuarios:borrar_usuario', kwargs={'id_usuario':deleted_user.id}))
        #Aqui checo la lista al acceder al nuevo url
        listresp = self.client.get(reverse('usuarios:lista_usuarios'))
        self.assertEqual(listresp.status_code, 200)

        self.assertEqual(len(listresp.context['usuarios']), 1)

        self.assertNotEqual(listresp.context['usuarios'], deleted_user.username)

        # resp4 = self.client.get(reverse('usuarios:lista_usuarios'))
        # self.assertEqual(len(resp4.context['usuarios']), 1)

class TestTerminarSesion(TestCase):

    def setUp(self):
        #El setup sirve para crear un usuario en la base de datos, pero no inicia sesion
        Group.objects.create(name="admin")
        user = User.objects.create_user(username='temporary', email='temporary@gmail.com', password='temporary', is_superuser='True')
        #Guarda el usuario que se creó
        user.save()

    def test_ac47_1_cerrando_sesion_no_accede_a_vistas_protegidas(self):
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #se cierra la sesion
        self.client.get("/logout")
        #se intenta iniciar sesion sin usuario
        response_sin_usuario = self.client.get(reverse('usuarios:lista_usuarios'))
        self.assertEqual(response_sin_usuario.status_code, 200)

    def test_ac47_2_cerrando_sesion_te_manda_al_logout(self):
        self.client.login(username='temporary', password='temporary')
        #Guardo la respuesta en resp
        resp = self.client.get(reverse('usuarios:lista_usuarios'))
        #Respuesta exitosa
        self.assertEqual(resp.status_code, 200)
        #se cierra la sesion
        self.client.get("/logout")
        #se intenta iniciar sesion sin usuario
        response_sin_usuario = self.client.get(reverse('materiales:materiales'))
        self.assertEqual(response_sin_usuario.status_code, 200)
