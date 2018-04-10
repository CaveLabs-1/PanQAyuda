from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mermas'

urlpatterns = [
    path('', views.lista_mermas, name='lista_mermas'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
