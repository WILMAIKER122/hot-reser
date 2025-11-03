import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def generar_codigo_reserva():
    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(9))
    return codigo

class Cliente(models.Model):  # Cambiado a Cliente (singular)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Habitacion(models.Model):
    TIPO_HABITACION = [
        ('Lujo', 'Lujo'),
        ('Estándar', 'Estándar'),
        ('Económica', 'Económica'),
    ]
    
    TIPO_CAMA = [
        ('Matrimonial', 'Matrimonial'),
        ('Individual', 'Individual'),
        ('Litera', 'Litera'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_HABITACION)
    numero = models.IntegerField(unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    seleccionada = models.BooleanField(default=False)

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"

class Reservacion(models.Model):  # Nombre en singular
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservaciones')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Relación con User de Django
    fecha_entrada = models.DateTimeField()
    fecha_salida = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    codigo_reserva = models.CharField(
        max_length=9,
        unique=True,
        default=generar_codigo_reserva,
        editable=False,
    )

    def __str__(self):
        return f'Reserva #{self.id} - {self.cliente}'
    
    def save(self, *args, **kwargs):
        if not self.id: 
            codigo = generar_codigo_reserva()
            while Reservacion.objects.filter(codigo_reserva=codigo).exists():
                codigo = generar_codigo_reserva()
            self.codigo_reserva = codigo
        super(Reservacion, self).save(*args, **kwargs)

# =============================================
# NUEVOS MODELOS PARA LOS MÓDULOS AGREGADOS
# =============================================

class UserProfile(models.Model):
    """
    Perfil extendido para usuarios/estudiantes
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Información académica
    institution = models.CharField(max_length=200, default='UTD Francisco Tamayo')
    semester = models.IntegerField(default=1, choices=[(i, f'{i}° Semestre') for i in range(1, 7)])
    career = models.CharField(max_length=100, default='Turismo')
    specialization = models.CharField(
        max_length=50,
        choices=[
            ('recepcion', 'Recepción Hotelera'),
            ('reservas', 'Gestión de Reservas'),
            ('eventos', 'Organización de Eventos'),
            ('alimentos', 'Alimentos y Bebidas'),
        ],
        default='recepcion'
    )
    
    # Avatar
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Preferencias de notificación
    email_notifications = models.BooleanField(default=True)
    practice_reminders = models.BooleanField(default=True)
    progress_updates = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=False)
    
    # Estadísticas (podrían calcularse automáticamente)
    total_simulations = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    achievements_unlocked = models.IntegerField(default=0)
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

class SystemSettings(models.Model):
    """
    Configuración global del sistema
    """
    # Información de la institución
    institution_name = models.CharField(max_length=200, default='Turismo Hospitality')
    institution_slogan = models.CharField(max_length=300, default='Excelencia en Educación Turística')
    contact_email = models.EmailField(default='contacto@turismohospitality.edu')
    contact_phone = models.CharField(max_length=20, default='+58 123-456-7890')
    
    # Configuración académica
    simulation_duration = models.IntegerField(default=30, help_text="Duración en minutos")
    max_attempts = models.IntegerField(default=3, help_text="Intentos máximos por simulación")
    passing_score = models.IntegerField(default=70, help_text="Puntuación mínima para aprobar")
    max_students = models.IntegerField(default=500, help_text="Límite de estudiantes activos")
    
    # Configuración regional
    LANGUAGE_CHOICES = [
        ('es', 'Español'),
        ('en', 'English'),
        ('pt', 'Português'),
    ]
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='es')
    
    TIMEZONE_CHOICES = [
        ('America/Caracas', 'Caracas (UTC-4)'),
        ('America/Mexico_City', 'Ciudad de México (UTC-6)'),
        ('America/Bogota', 'Bogotá (UTC-5)'),
    ]
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='America/Caracas')
    
    DATE_FORMAT_CHOICES = [
        ('dd/mm/yyyy', 'DD/MM/AAAA'),
        ('mm/dd/yyyy', 'MM/DD/AAAA'),
        ('yyyy-mm-dd', 'AAAA-MM-DD'),
    ]
    date_format = models.CharField(max_length=10, choices=DATE_FORMAT_CHOICES, default='dd/mm/yyyy')
    
    CURRENCY_CHOICES = [
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
        ('VES', 'VES (Bs.)'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='VES')
    
    # Apariencia
    THEME_CHOICES = [
        ('default', 'Tema Predeterminado'),
        ('dark', 'Tema Oscuro'),
        ('ocean', 'Tema Océano'),
        ('nature', 'Tema Naturaleza'),
    ]
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')
    
    # Configuración del sistema
    email_notifications = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    auto_backup = models.BooleanField(default=False)
    backup_frequency = models.CharField(
        max_length=10,
        choices=[('daily', 'Diario'), ('weekly', 'Semanal'), ('monthly', 'Mensual')],
        default='weekly'
    )
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Configuración del Sistema"
    
    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"

class BackupHistory(models.Model):
    """
    Historial de backups del sistema
    """
    filename = models.CharField(max_length=255)
    size = models.BigIntegerField(help_text="Tamaño en bytes")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Backup {self.filename} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "Historial de Backup"
        verbose_name_plural = "Historial de Backups"
        ordering = ['-created_at']