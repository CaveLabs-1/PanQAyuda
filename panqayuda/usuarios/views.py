from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from panqayuda.decorators import group_required
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import FormUser

"""
    Función que enlista todos los usuarios guardadas dentro de la base de datos y guarda nuevos usuarios.
    Regresa objetos de usuario.
"""

@group_required('admin')
def lista_usuarios(request):
    # En caso de que exista una petición de tipo POST significa que se ha intentado dar de alta un nuevo usuario.
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_superuser = request.POST.get('is_superuser')
        is_staff = request.POST.get('is_staff') or False
        if is_staff == 1:
            is_staff = True
        else:
            is_staff=False

        if is_superuser == 'on':
            is_superuser = True
        else:
            is_superuser=False
        password = request.POST.get('password')
        user = User.objects.create(username=username, email=email, first_name=first_name,
                                            last_name=last_name, is_superuser=is_superuser,
                                            is_staff=is_staff)
        if user:
            user.set_password(password)
            user.save()
        else:
            User.objects.filter(user).delete()


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
        usuarios =  User.objects.filter(is_active=1)
        # Se muestra la lista de usuarios con una forma disponible para dar de alta uno nuevo.
        return render (request, 'lista_usuarios.html', {'forma': forma, 'usuarios': usuarios})


"""
    Función para eliminar usuarios de la base de datos (soft delete).
"""
@group_required('admin')
def borrar_usuario(request, id_usuario):
    #recuperar el usuario
    usuario = get_object_or_404(User, pk=id_usuario)
    #soft delete django
    usuario.is_active = 0
    usuario.save()
    #mensaje de éxito
    messages.success(request, '¡Se ha eliminado al usuario!')
    return redirect('usuarios:lista_usuarios')
