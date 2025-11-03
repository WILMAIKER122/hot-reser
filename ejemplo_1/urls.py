# ejemplo_1/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns, set_language

urlpatterns = i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    
    # INCLUYE las URLs de la aplicación 'myapp'
    # La ruta raíz '' significa que las URLs de myapp (dashboard/, login/, etc.) 
    # se acceden directamente después de la dirección del servidor (ej: /dashboard/)
    path('', include('myapp.urls')),
)