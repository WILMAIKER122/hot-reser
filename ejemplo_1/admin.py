from django.contrib import admin
from myapp.models import Cliente, Habitacion, Reservacion, UserProfile, SystemSettings, BackupHistory

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

# =============================================
# NUEVOS ADMIN PARA LOS MODELOS AGREGADOS
# =============================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'semester', 'career', 'specialization']
    search_fields = ['user__username', 'user__email', 'institution']
    list_filter = ['semester', 'career', 'specialization']

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['institution_name', 'language', 'timezone', 'theme']
    
    def has_add_permission(self, request):
        # Solo permitir una configuración del sistema
        return not SystemSettings.objects.exists()

@admin.register(BackupHistory)
class BackupHistoryAdmin(admin.ModelAdmin):
    list_display = ['filename', 'size', 'created_by', 'created_at']
    readonly_fields = ['created_at']
    list_filter = ['created_at']
    search_fields = ['filename']