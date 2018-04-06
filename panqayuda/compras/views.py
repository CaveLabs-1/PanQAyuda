from django.shortcuts import render

# Create your views here.

def lista_detalle_compra(request):
    if request.method == 'POST':
        id_compra = request.POST.get('id_compra')
        compra = Venta.objects.get(pk=id_compra)
        materiales_de_compra = RelacionVentaPaquete.objects.filter(compra=compra)
        response = render_to_string('compras/lista_detalle_compra.html', {'materiales_de_compra': materiales_de_compra, 'compra': compra})
        return HttpResponse(response)
    return HttpResponse('Algo ha salido mal.')
