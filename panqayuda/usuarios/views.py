from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from panqayuda.decorators import group_required
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import FormUser
from django.utils import timezone
from django.contrib.auth.models import Group

"""
    Función que enlista todos los usuarios guardadas dentro de la base de datos y guarda nuevos usuarios.
    Regresa objetos de usuario.
"""

@group_required('superadmin')
def lista_usuarios(request):
    # En caso de que exista una petición de tipo POST significa que se ha intentado dar de alta un nuevo usuario.
    if request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            usuario = form.save()
            if usuario.is_staff == 1:
                usuario.is_staff = True
            else:
                usuario.is_staff=False

            if usuario.is_superuser == True:
                usuario.nombre_grupo = 'superadmin'
                #usuario.is_superuser = True
            else:
                usuario.nombre_grupo = 'admin'
                usuario.is_superuser=False
            usuario.set_password(usuario.password)
            usuario.save()
            # user = User.objects.create(username=username, password=password, email=email, first_name=first_name,
            #                                     last_name=last_name, is_superuser=is_superuser,
            #                                     is_staff=is_staff)
            #Añadir usuario al grupo correspondiente
            grupo = Group.objects.get(name=usuario.nombre_grupo)
            grupo.user_set.add(usuario)
            grupo.save()
        else:
            form = FormUser()


        # forma_post = FormUser(request.POST)
        # # Si la forma es válida, se guarda el nuevo usuario y devuelve mensaje de éxito.
        # if forma_post.is_valid():
        #     forma_post.save()
        #     messages.success(request, 'Se ha agregado un nuevo usuario.')
        # #se llama a sí mismo para pintar la lista de usuarios con una nueva forma para dar de alta otro usuario.
        return HttpResponseRedirect(reverse('usuarios:lista_usuarios'))
    # En caso de que no haya ninguna petición
    else:
        # Se crea una nueva forma para dar de alta un usuario.
        forma = FormUser()
        # Se obtiene la lista de usuairos.
        usuarios =  User.objects.filter(is_active=True)

        # Se muestra la lista de usuarios con una forma disponible para dar de alta uno nuevo.
        return render (request, 'lista_usuarios.html', {'forma': forma, 'usuarios': usuarios})


"""
    Función para eliminar usuarios de la base de datos (soft delete).
"""
@group_required('superadmin')
def borrar_usuario(request, id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    #soft delete django
    usuario_nombre = usuario.username
    usuario.username = usuario_nombre + "deleted" + str(timezone.now)
    usuario.is_active = False
    usuario.is_superuser=False
    usuario.save()
    messages.success(request, '¡Se ha eliminado al usuario!')
    return redirect('usuarios:lista_usuarios')
