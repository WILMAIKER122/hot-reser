from django.core.management.base import BaseCommand
from myapp.models import Cliente, Habitacion, Reservacion
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Carga datos iniciales para el sistema'
    
    def handle(self, *args, **options):
        self.stdout.write("Creando datos de prueba...")
        
        # Crear usuario admin
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@hotel.com',
            password='admin123'
        )
        
        # Crear clientes
        clientes = [
            {'nombre': 'Ana', 'apellido': 'García', 'cedula': '001-1234567-8', 'telefono': '809-555-0101', 'email': 'ana@example.com'},
            {'nombre': 'Carlos', 'apellido': 'Rodríguez', 'cedula': '002-9876543-2', 'telefono': '809-555-0202', 'email': 'carlos@example.com'}
        ]
        
        for cliente_data in clientes:
            Cliente.objects.get_or_create(**cliente_data)
        
        # Crear habitaciones
        tipos_habitacion = [choice[0] for choice in Habitacion.TIPO_HABITACION]
        tipos_cama = [choice[0] for choice in Habitacion.TIPO_CAMA]
        
        for i in range(1, 11):
            Habitacion.objects.create(
                numero=100 + i,
                tipo=random.choice(tipos_habitacion),
                precio=random.randint(1500, 5000),
                disponible=random.choice([True, False])
            )
        
        # Crear reservaciones
        clientes = Cliente.objects.all()
        habitaciones = Habitacion.objects.filter(disponible=True)
        
        for i in range(5):
            Reservacion.objects.create(
                cliente=random.choice(clientes),
                habitacion=random.choice(habitaciones),
                usuario_registro=admin_user,
                fecha_entrada=datetime.now() + timedelta(days=i),
                fecha_salida=datetime.now() + timedelta(days=i + random.randint(1, 5))
            )
        
        self.stdout.write(self.style.SUCCESS('Datos creados exitosamente!'))