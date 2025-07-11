from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register, name='registro'),
    path('cerrar_sesion/', views.custom_logout_view, name='cerrar_sesion'), 
    path('lista_habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('reservacion/', views.reservacion, name='reservacion'),
    path('seleccionar_habitacion/<int:habitacion_id>/', views.seleccionar_habitacion, name='seleccionar_habitacion'),
    path('lista_reservaciones/', views.lista_reservaciones, name='lista_reservaciones'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar_cliente', views.registrar_cliente, name='registrar_cliente'),
]