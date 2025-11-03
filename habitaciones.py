import os
import django
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from myapp.models import Habitacion

def crear_habitaciones():
    """Función para crear habitaciones de ejemplo para un hotel educativo"""
    
    habitaciones = [
        # === SUITES DE LUJO (Piso 1) ===
        {'tipo': 'Lujo', 'numero': 101, 'precio': 350.00, 'piso': 1},
        {'tipo': 'Lujo', 'numero': 102, 'precio': 350.00, 'piso': 1},
        {'tipo': 'Lujo', 'numero': 103, 'precio': 400.00, 'piso': 1},  # Suite Presidencial
        {'tipo': 'Lujo', 'numero': 104, 'precio': 400.00, 'piso': 1},  # Suite Presidencial
        
        # === HABITACIONES EJECUTIVAS (Piso 2) ===
        {'tipo': 'Lujo', 'numero': 201, 'precio': 280.00, 'piso': 2},
        {'tipo': 'Lujo', 'numero': 202, 'precio': 280.00, 'piso': 2},
        {'tipo': 'Lujo', 'numero': 203, 'precio': 280.00, 'piso': 2},
        {'tipo': 'Lujo', 'numero': 204, 'precio': 280.00, 'piso': 2},
        
        # === HABITACIONES ESTÁNDAR DOBLES (Piso 3) ===
        {'tipo': 'Estándar', 'numero': 301, 'precio': 180.00, 'piso': 3},
        {'tipo': 'Estándar', 'numero': 302, 'precio': 180.00, 'piso': 3},
        {'tipo': 'Estándar', 'numero': 303, 'precio': 180.00, 'piso': 3},
        {'tipo': 'Estándar', 'numero': 304, 'precio': 180.00, 'piso': 3},
        {'tipo': 'Estándar', 'numero': 305, 'precio': 180.00, 'piso': 3},
        {'tipo': 'Estándar', 'numero': 306, 'precio': 180.00, 'piso': 3},
        
        # === HABITACIONES ESTÁNDAR INDIVIDUALES (Piso 4) ===
        {'tipo': 'Estándar', 'numero': 401, 'precio': 120.00, 'piso': 4},
        {'tipo': 'Estándar', 'numero': 402, 'precio': 120.00, 'piso': 4},
        {'tipo': 'Estándar', 'numero': 403, 'precio': 120.00, 'piso': 4},
        {'tipo': 'Estándar', 'numero': 404, 'precio': 120.00, 'piso': 4},
        {'tipo': 'Estándar', 'numero': 405, 'precio': 120.00, 'piso': 4},
        
        # === HABITACIONES ECONÓMICAS (Piso 5) ===
        {'tipo': 'Económica', 'numero': 501, 'precio': 80.00, 'piso': 5},
        {'tipo': 'Económica', 'numero': 502, 'precio': 80.00, 'piso': 5},
        {'tipo': 'Económica', 'numero': 503, 'precio': 80.00, 'piso': 5},
        {'tipo': 'Económica', 'numero': 504, 'precio': 80.00, 'piso': 5},
        {'tipo': 'Económica', 'numero': 505, 'precio': 80.00, 'piso': 5},
        {'tipo': 'Económica', 'numero': 506, 'precio': 80.00, 'piso': 5},
        {'tipo': 'Económica', 'numero': 507, 'precio': 80.00, 'piso': 5},
        {'tipo': 'Económica', 'numero': 508, 'precio': 80.00, 'piso': 5},
    ]
    
    creadas = 0
    existentes = 0
    errores = 0
    
    print("🏨 INICIANDO CREACIÓN DE HABITACIONES...")
    print("=" * 50)
    
    for habitacion_data in habitaciones:
        try:
            # Verificar si la habitación ya existe
            if not Habitacion.objects.filter(numero=habitacion_data['numero']).exists():
                Habitacion.objects.create(
                    tipo=habitacion_data['tipo'],
                    numero=habitacion_data['numero'],
                    precio=habitacion_data['precio'],
                    disponible=True,
                    seleccionada=False
                )
                creadas += 1
                print(f'✅ Creada: Habitación {habitacion_data["numero"]} - {habitacion_data["tipo"]} - ${habitacion_data["precio"]}')
            else:
                existentes += 1
                print(f'⚠️ Ya existe: Habitación {habitacion_data["numero"]}')
                
        except Exception as e:
            errores += 1
            print(f'❌ Error en habitación {habitacion_data["numero"]}: {str(e)}')
    
    # Estadísticas finales
    print("=" * 50)
    print("📊 RESUMEN FINAL:")
    print(f"✅ Habitaciones creadas: {creadas}")
    print(f"⚠️ Habitaciones existentes: {existentes}")
    print(f"❌ Errores: {errores}")
    print(f"🏨 Total en sistema: {Habitacion.objects.count()}")
    
    # Estadísticas por tipo
    print("\n📈 DISTRIBUCIÓN POR TIPO:")
    for tipo in ['Lujo', 'Estándar', 'Económica']:
        count = Habitacion.objects.filter(tipo=tipo).count()
        print(f"   {tipo}: {count} habitaciones")
    
    # Habitaciones disponibles vs ocupadas
    disponibles = Habitacion.objects.filter(disponible=True).count()
    ocupadas = Habitacion.objects.filter(disponible=False).count()
    print(f"\n🎯 DISPONIBILIDAD:")
    print(f"   Disponibles: {disponibles}")
    print(f"   Ocupadas: {ocupadas}")

if __name__ == '__main__':
    crear_habitaciones()