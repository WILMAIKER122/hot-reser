import os
import django
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from myapp.models import Cliente

def crear_clientes():
    """Función para crear clientes de ejemplo para prácticas de turismo"""
    
    # Datos de clientes diversos para simulaciones realistas
    clientes_data = [
        # === CLIENTES NACIONALES ===
        {
            'nombre': 'María', 'apellido': 'González', 
            'cedula': 'V-12345678', 'telefono': '+58-412-555-0101',
            'email': 'maria.gonzalez@email.com'
        },
        {
            'nombre': 'Carlos', 'apellido': 'Rodríguez', 
            'cedula': 'V-23456789', 'telefono': '+58-414-555-0102',
            'email': 'carlos.rodriguez@email.com'
        },
        {
            'nombre': 'Ana', 'apellido': 'López', 
            'cedula': 'V-34567890', 'telefono': '+58-416-555-0103',
            'email': 'ana.lopez@email.com'
        },
        {
            'nombre': 'José', 'apellido': 'Pérez', 
            'cedula': 'V-45678901', 'telefono': '+58-424-555-0104',
            'email': 'jose.perez@email.com'
        },
        {
            'nombre': 'Laura', 'apellido': 'Hernández', 
            'cedula': 'V-56789012', 'telefono': '+58-426-555-0105',
            'email': 'laura.hernandez@email.com'
        },
        
        # === CLIENTES INTERNACIONALES ===
        {
            'nombre': 'John', 'apellido': 'Smith', 
            'cedula': 'P-98765432', 'telefono': '+1-555-010-1001',
            'email': 'john.smith@international.com'
        },
        {
            'nombre': 'Sophie', 'apellido': 'Martin', 
            'cedula': 'P-87654321', 'telefono': '+33-1-5555-0102',
            'email': 'sophie.martin@email.fr'
        },
        {
            'nombre': 'Carlos', 'apellido': 'Silva', 
            'cedula': 'P-76543210', 'telefono': '+55-11-5555-0103',
            'email': 'carlos.silva@email.com.br'
        },
        {
            'nombre': 'Elena', 'apellido': 'Rossi', 
            'cedula': 'P-65432109', 'telefono': '+39-02-5555-0104',
            'email': 'elena.rossi@email.it'
        },
        
        # === CLIENTES CORPORATIVOS ===
        {
            'nombre': 'Roberto', 'apellido': 'Mendoza', 
            'cedula': 'V-11223344', 'telefono': '+58-212-555-0201',
            'email': 'roberto.mendoza@empresa.com'
        },
        {
            'nombre': 'Patricia', 'apellido': 'Castillo', 
            'cedula': 'V-22334455', 'telefono': '+58-212-555-0202',
            'email': 'patricia.castillo@corporacion.com'
        },
        
        # === CLIENTES CON NECESIDADES ESPECIALES ===
        {
            'nombre': 'Miguel', 'apellido': 'Torres', 
            'cedula': 'V-33445566', 'telefono': '+58-414-555-0301',
            'email': 'miguel.torres@email.com'
        },
        {
            'nombre': 'Isabel', 'apellido': 'Rojas', 
            'cedula': 'V-44556677', 'telefono': '+58-416-555-0302',
            'email': 'isabel.rojas@email.com'
        },
        
        # === CLIENTES FRECUENTES ===
        {
            'nombre': 'Diego', 'apellido': 'Fernández', 
            'cedula': 'V-55667788', 'telefono': '+58-424-555-0401',
            'email': 'diego.fernandez@email.com'
        },
        {
            'nombre': 'Carmen', 'apellido': 'Navarro', 
            'cedula': 'V-66778899', 'telefono': '+58-426-555-0402',
            'email': 'carmen.navarro@email.com'
        },
        
        # === CLIENTES CON RESERVAS GRUPALES ===
        {
            'nombre': 'Ricardo', 'apellido': 'Vargas', 
            'cedula': 'V-77889900', 'telefono': '+58-414-555-0501',
            'email': 'ricardo.vargas@email.com'
        },
        {
            'nombre': 'Gabriela', 'apellido': 'Morales', 
            'cedula': 'V-88990011', 'telefono': '+58-416-555-0502',
            'email': 'gabriela.morales@email.com'
        },
        
        # === CLIENTES DE ÚLTIMA HORA ===
        {
            'nombre': 'Fernando', 'apellido': 'Castro', 
            'cedula': 'V-99001122', 'telefono': '+58-424-555-0601',
            'email': 'fernando.castro@email.com'
        },
        {
            'nombre': 'Adriana', 'apellido': 'Romero', 
            'cedula': 'V-10111213', 'telefono': '+58-426-555-0602',
            'email': 'adriana.romero@email.com'
        },
        
        # === CLIENTES CON PREFERENCIAS ESPECÍFICAS ===
        {
            'nombre': 'Oscar', 'apellido': 'Díaz', 
            'cedula': 'V-12131415', 'telefono': '+58-414-555-0701',
            'email': 'oscar.diaz@email.com'
        },
        {
            'nombre': 'Lucía', 'apellido': 'Ortega', 
            'cedula': 'V-13141516', 'telefono': '+58-416-555-0702',
            'email': 'lucia.ortega@email.com'
        },
    ]
    
    creados = 0
    existentes = 0
    errores = 0
    
    print("👥 INICIANDO CREACIÓN DE CLIENTES...")
    print("=" * 50)
    
    for cliente_data in clientes_data:
        try:
            # Verificar si el cliente ya existe por cédula
            if not Cliente.objects.filter(cedula=cliente_data['cedula']).exists():
                Cliente.objects.create(
                    nombre=cliente_data['nombre'],
                    apellido=cliente_data['apellido'],
                    cedula=cliente_data['cedula'],
                    telefono=cliente_data['telefono'],
                    email=cliente_data['email']
                )
                creados += 1
                print(f'✅ Creado: {cliente_data["nombre"]} {cliente_data["apellido"]} - {cliente_data["cedula"]}')
            else:
                existentes += 1
                print(f'⚠️ Ya existe: {cliente_data["nombre"]} {cliente_data["apellido"]} - {cliente_data["cedula"]}')
                
        except Exception as e:
            errores += 1
            print(f'❌ Error en cliente {cliente_data["nombre"]} {cliente_data["apellido"]}: {str(e)}')
    
    # Estadísticas finales
    print("=" * 50)
    print("📊 RESUMEN FINAL:")
    print(f"✅ Clientes creados: {creados}")
    print(f"⚠️ Clientes existentes: {existentes}")
    print(f"❌ Errores: {errores}")
    print(f"👥 Total en sistema: {Cliente.objects.count()}")
    
    # Mostrar algunos clientes creados
    print("\n🎯 MUESTRA DE CLIENTES CREADOS:")
    clientes_recientes = Cliente.objects.all().order_by('-id')[:5]
    for cliente in clientes_recientes:
        print(f"   👤 {cliente.nombre} {cliente.apellido} - {cliente.cedula}")

def crear_clientes_adicionales(cantidad=10):
    """Función para crear clientes adicionales de forma aleatoria"""
    print(f"\n🎲 CREANDO {cantidad} CLIENTES ADICIONALES ALEATORIOS...")
    print("=" * 50)
    
    nombres = ['Luis', 'Marta', 'Javier', 'Sandra', 'Pedro', 'Rosa', 'Andrés', 'Claudia', 'Raúl', 'Verónica']
    apellidos = ['García', 'Martínez', 'Jiménez', 'Moreno', 'Rubio', 'Santos', 'Cruz', 'Flores', 'Vega', 'Campos']
    
    adicionales_creados = 0
    
    for i in range(cantidad):
        try:
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            cedula = f"V-{random.randint(20000000, 30000000)}"
            
            if not Cliente.objects.filter(cedula=cedula).exists():
                Cliente.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    cedula=cedula,
                    telefono=f"+58-{random.randint(412, 426)}-555-{random.randint(1000, 9999):04d}",
                    email=f"{nombre.lower()}.{apellido.lower()}@ejemplo.com"
                )
                adicionales_creados += 1
                print(f'✅ Adicional: {nombre} {apellido} - {cedula}')
                
        except Exception as e:
            print(f'❌ Error en cliente adicional: {str(e)}')
    
    print(f"🎲 Clientes adicionales creados: {adicionales_creados}")
    print(f"👥 Total final: {Cliente.objects.count()}")

if __name__ == '__main__':
    crear_clientes()
    crear_clientes_adicionales(5)  # Crea 5 clientes adicionales aleatorios