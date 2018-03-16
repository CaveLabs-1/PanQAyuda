from django.test import TestCase
from django.urls import reverse
from proveedores.models import Proveedor

#Test agregar proveedor
class TestAgregarProveedor(TestCase):

    #Checa si existe la vista (template) para agregar el proveedor
    def test_existe_vista(self):
        resp = self.client.get(reverse('proveedores:agregar_proveedor'))
        self.assertEqual(resp.status_code, 200)

    #Checa si existe un objeto anteriormente, despues le manda una forma con informacion valida y checa si se guardó
    def test_ac1_el_proveedor_se_agrega_exitosamente(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 1)

    #checa que el nombre no este vacio
    def test_ac2_nombre_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el telefono tenga formato correcto
    def test_ac3_formato_telefono(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4155, 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el telefono no este vacio
    def test_ac4_telefono_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que la direccion no este vacia
    def test_ac5_direccion_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que el rfc no este vacio
    def test_ac6_rfc_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
        self.assertEqual(Proveedor.objects.count(), 0)

    #checa que la razon social no este vacia
    def test_ac7_razon_social_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'rfc':45321343, 'email':"ejemplo@hotmail.com" }
        self.client.post(reverse('proveedores:agregar_proveedor'), data)
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
        resp = self.client.post(reverse('proveedor:agregar_proveedor'), data)
        self.assertEqual(Paquete.objects.count(), 0)
        self.assertFormError(resp, 'form', 'nombre', "Debes introducir un nombre.")

    #retorno de error al dejar campo telefono vacio
    def test_ac11_retorno_error_campo_telefono_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'direccion':"calle 100 corazones", 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedor:agregar_proveedor'), data)
        self.assertEqual(Paquete.objects.count(), 0)
        self.assertFormError(resp, 'form', 'nombre', "Debes introducir un telefono.")

    #retorno de error al dejar campo direccion vacio
    def test_ac12_retorno_error_campo_direccion_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'rfc':45321343, 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedor:agregar_proveedor'), data)
        self.assertEqual(Paquete.objects.count(), 0)
        self.assertFormError(resp, 'form', 'nombre', "Debes poner una direccion.")

    #retorno error al dejar rfc vacio
    def test_ac13_retorno_error_campo_rfc_vacio(self):
        self.assertEqual(Proveedor.objects.count(), 0)
        data = {'nombre':"Bancomer", 'telefono':4151043944, 'direccion':"calle 100 corazones", 'razon_social':"Somos unos cracks", 'email':"ejemplo@hotmail.com" }
        resp = self.client.post(reverse('proveedor:agregar_proveedor'), data)
        self.assertEqual(Paquete.objects.count(), 0)
        self.assertFormError(resp, 'form', 'nombre', "Debes introducir un nombre.")

# Create your tests here.
