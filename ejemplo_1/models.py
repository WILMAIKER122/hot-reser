from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return f'Reserva #{self.id} - {self.cliente}'