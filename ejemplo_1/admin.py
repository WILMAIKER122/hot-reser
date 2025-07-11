from django.contrib import admin
from .models import Cliente, Habitacion, Reservacion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'telefono', 'email')
    search_fields = ('nombre', 'apellido', 'cedula')
    list_filter = ('nombre', 'apellido')

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'precio', 'disponible', 'seleccionada')
    list_filter = ('tipo', 'disponible', 'seleccionada')
    search_fields = ('numero',)
    list_editable = ('disponible', 'seleccionada')

@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'usuario_registro')
    list_filter = ('fecha_entrada', 'fecha_salida')
    raw_id_fields = ('cliente', 'habitacion')
    date_hierarchy = 'fecha_entrada'