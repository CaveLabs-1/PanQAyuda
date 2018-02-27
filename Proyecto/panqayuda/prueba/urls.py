from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prueba'

urlpatterns = [
    path('prueba_view/', views.prueba_view, name='prueba_view')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
