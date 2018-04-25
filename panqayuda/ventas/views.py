from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import VentaForm, RelacionVentaPaqueteForm
from .models import Venta, RelacionVentaPaquete
from django.contrib import messages
from paquetes.models import Paquete, PaqueteInventario
from clientes.forms import FormCliente
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.db.models import Sum
from panqayuda.decorators import group_required
from functools import reduce
import datetime

"""
    View para mostrar la lista de ventas, con forma disponible para crear una nueva ventas.
"""
@group_required('admin')
def ventas(request):
    if request.method == 'POST':
        forma_post = VentaForm(request.POST)
        if forma_post.is_valid():
            forma_post.save()
            messages.success(request, 'Se ha agregado una nueva venta.')
        else:
            messages.error(request, 'Hubo un error, inténtalo de nuevo.')

        return HttpResponseRedirect(reverse('ventas:ventas'))
    else:
        forma = VentaForm()
        ventas =  Venta.objects.filter(deleted_at__isnull=True)
        return render (request, 'ventas/ventas.html', {'forma': forma, 'ventas': ventas})

"""
    Recibe una venta y detalla la información sobre ella
"""
@group_required('admin')
def lista_detalle_venta(request):
    if request.method == 'POST':
        id_venta = request.POST.get('id_venta')
        venta = Venta.objects.get(pk=id_venta)
        paquetes_de_venta = RelacionVentaPaquete.objects.filter(venta=venta)
        response = render_to_string('ventas/lista_detalle_venta.html', {'paquetes_de_venta': paquetes_de_venta, 'venta': venta})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')

"""
    Genera una nueva venta
"""
@group_required('admin')
def generar_venta(request):
    if request.method == "POST":
        forma_venta = VentaForm(request.POST)
        if forma_venta.is_valid():
            #Guardar la venta para después asignarsela a la relación venta-paquete
            forma_venta = forma_venta.save(commit=False)
            #Extraer la lista de paquetes y su respectiva cantidad de la venta
            paquetes = request.POST.getlist('paquete')
            cantidades = request.POST.getlist('cantidad')
            #Variable que se usará para guardar las relaciones venta-paquete
            lista_relaciones = []
            #Validar las relaciones paquete-venta
            if len(paquetes)==len(cantidades):
                if len(paquetes) != 0:
                    for i in range(len(paquetes)):
                        paquete = get_object_or_404(Paquete, pk=paquetes[i])
                        cantidad = int(cantidades[i])
                        #Verificar que haya suficiente <cantidad> en inventario para el paquete <paquete>
                        if paquete.obtener_disponibles_inventario() >= cantidad:
                            #Sí hay suficiente cantidad
                            data = {'paquete':paquete.id, 'cantidad':cantidad}
                            forma_paquete_venta = RelacionVentaPaqueteForm(data)
                            if forma_paquete_venta.is_valid():
                                #Asignarle el monto
                                forma_paquete_venta.instance.monto = paquete.precio * cantidad
                                #Agregar a la lista de relaciones para guardar al final
                                lista_relaciones.append(forma_paquete_venta.save(commit=False))
                            else:
                                messages.error(request, 'Hubo un error con la forma. Inténtalo de nuevo.')
                                return redirect('ventas:generar_venta')
                        else:
                            #No hay suficiente cantidad
                            messages.error(request, 'No hay suficiente cantidad en inventario para el paquete ' + paquete.nombre)
                            return redirect('ventas:generar_venta')
                    #Asignarle monto total a la venta
                    monto_total = 0
                    for relacion in lista_relaciones:
                        monto_total += relacion.monto
                    forma_venta.monto_total = monto_total
                    #Guardar Venta
                    forma_venta.save()

                    #Guardar las relaciones en la base de datos
                    for relacion in lista_relaciones:
                        # Asignar id de venta a esta relación
                        relacion.venta = forma_venta
                        relacion.save()

                    #Restar paquetes de inventario
                    for relacion in lista_relaciones:
                        restar_paquetes_inventario(relacion.paquete, relacion.cantidad)

                    messages.success(request, "¡La venta se ha generado con éxito!")
                    return redirect('ventas:generar_venta')
                else:
                    messages.error(request, 'Hubo un error con la forma. Inténtanlo de nuevo.')
                    return redirect('ventas:generar_venta')
            else:
                #no se seleccionó ningún paquete
                messages.error(request, 'Debes seleccionar al menos un paquete para que se genera la venta.')
                return redirect('ventas:generar_venta')
    else:
        #La forma que contiene el campo para seleccionar al cliente
        forma_venta = VentaForm()
        #La forma para cada paquete que se genera en la venta
        forma_paquete_venta = RelacionVentaPaqueteForm()
        forma_paquete_venta.fields['paquete'].queryset = Paquete.objects.filter(deleted_at__isnull=True)
        #La forma en caso de que se quiera agregar un nuevo cliente
        forma_cliente = FormCliente()
        data = {'forma_venta':forma_venta, 'forma_paquete_venta':forma_paquete_venta, 'forma':forma_cliente}
        return render(request, 'ventas/agregar_venta.html',data)

def restar_paquetes_inventario(paquete,cantidad):
    # Obtener paquetes del inventario disponibles para restar ordenados por fecha de caducidad
    paquetes_inventario = paquete.obtener_paquetes_inventario_disponibles()
    for paquete_inventario in paquetes_inventario:
        # La necesitada es mayor que la cantidad que este 'lote' tiene
        if cantidad > paquete_inventario.disponible:
            cantidad -= paquete_inventario.disponible
            paquete_inventario.ocupados = paquete_inventario.cantidad
            paquete_inventario.save()
        # Este 'lote' satisface la cantidad necesitada para el paquete
        else:
            paquete_inventario.ocupados += cantidad
            paquete_inventario.save()
            break

#Verifica si hay suficientes paquetes disponibles para realizar la venta, devuelve una fila de la tabla
#para el resumen de venta.
@group_required('admin')
def agregar_paquete_a_venta(request):
    # Verificar que no se hayan dejado vacíos
    if request.GET.get('paquete') == "" or request.GET.get('cantidad') == "":
        return HttpResponseNotFound("Debes seleccionar una paquete y una cantidad.")

    #Obtener paquete y cantidad
    paquete = get_object_or_404(Paquete,pk=request.GET.get('paquete'))
    cantidad = int(request.GET.get('cantidad'))
    #Hay suficientes paquetes
    if paquete.obtener_disponibles_inventario() >= cantidad:
        #Generar forma para mandar al template
        data = {'paquete':paquete.id, 'cantidad':cantidad}
        forma_venta = RelacionVentaPaqueteForm(data)
        if forma_venta.is_valid():
            #Asignarle el monto a la relación
            forma_venta.instance.monto = cantidad*paquete.precio
            #Generar html de respuesta
            response = render_to_string('ventas/agregar_paquete_venta_row.html',{'forma_venta':forma_venta})
            return HttpResponse(response)
        else:
            return HttpResponseNotFound("Verifica que seleccionaste un paquete y una cantidad mayor a 0.")
    return HttpResponseNotFound("No hay suficientes paquetes en inventario de " + paquete.nombre)

@group_required('admin')
def cancelar_venta(request, id_venta):
        #Checar que el objeto exista
        venta = get_object_or_404(Venta, pk=id_venta)
        relacion_venta_paquete = RelacionVentaPaquete.objects.filter(venta=venta)
        #Asignación de valores
        for registro in relacion_venta_paquete:
            paquete = registro.paquete
            cantidad = registro.cantidad
            paquete_inventario = get_object_or_404(PaqueteInventario, pk=paquete.id)
            paquete_inventario.ocupados -= cantidad
            paquete_inventario.save()
        #Cambio de Estatus y asignacipon de deleted_at
        relacion_venta_paquete.estatus = 0
        relacion_venta_paquete.deleted_at = datetime.datetime.now()
        venta.deleted_at = datetime.datetime.now()
        #Saves
        venta.save()
        messages.success(request, '¡Se ha cancelado exitosamente la venta!')
        return redirect('ventas:ventas')
