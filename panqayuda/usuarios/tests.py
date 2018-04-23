from django.test import TestCase
from django.urls import reverse
import datetime
from django.contrib.auth.models import User, Group

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
