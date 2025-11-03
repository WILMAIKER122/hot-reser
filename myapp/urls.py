# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns, set_language


# Rutas específicas de la aplicación van aquí
urlpatterns = i18n_patterns ( 
    path('set_language/', set_language, name='set_language'),
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register, name='registro'),
    path('cerrar_sesion/', views.custom_logout_view, name='cerrar_sesion'), 
    path('lista_habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('reservacion/', views.reservacion, name='reservacion'),
    path('seleccionar_habitacion/<int:habitacion_id>/', views.seleccionar_habitacion, name='seleccionar_habitacion'),
    path('lista_reservaciones/', views.lista_reservaciones, name='lista_reservaciones'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('lista_cliente/', views.lista_cliente, name='lista_cliente'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar'),
    path('logout/', views.custom_logout_view, name='custom_logout_view'),

    path('perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    path('configuracion/', views.configuracion_sistema, name='configuracion_sistema'),
    
    path('api/upload-avatar/', views.upload_avatar, name='upload_avatar'),
    path('api/update-profile/', views.update_profile_data, name='update_profile'),
    path('api/save-settings/', views.save_system_settings, name='save_system_settings'),
    path('api/backup-system/', views.backup_system, name='backup_system'),
)

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)