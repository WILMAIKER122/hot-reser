# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import CustomUserCreationForm, LoginForm 
from .models import Cliente, Habitacion, Reservacion, UserProfile, SystemSettings, BackupHistory
from .form_reser import ClienteForm, ReservacionForm 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import connection
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.db.models import F, ExpressionWrapper, DurationField, IntegerField
from django.db.models.functions import Cast
from django.utils.timezone import localdate
from django.http import JsonResponse
import json
import os
from django.conf import settings

# para traducir 
from django.utils.translation import gettext as _

def index(request):
    show_warning = request.session.pop('show_logout_warning', False)
    return render(request, 'myapp/index.html', {'show_warning': show_warning})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, '⚠️ Nombre de usuario o contraseña no válidos')
        else:
            # Mostrar el primer error del formulario
            first_error = next(iter(form.errors.values()))[0]
            messages.error(request, first_error)
    else:
        next_url = request.GET.get('next')
        if next_url:
            messages.info(request, 'ℹ️ Debes iniciar sesión para continuar')
        form = LoginForm() 
    return render(request, 'myapp/login.html', {'form': form})

@login_required(login_url='/login/')
def dashboard(request):
    reservaciones = Reservacion.objects.all()
    total_ingresos = 0

    for reserva in reservaciones:
        noches = (reserva.fecha_salida.date() - reserva.fecha_entrada.date()).days
        total_ingresos += reserva.habitacion.precio * noches

    try:
        # Datos básicos con manejo de errores
        context = {
            'reservas_total': Reservacion.objects.filter(usuario_registro=request.user.id).count(),
            'cantidad_habitaciones': Habitacion.objects.count(),
            'clientes': Cliente.objects.count(),
            'total_ingresos': total_ingresos,  # Temporalmente fijo
            'reservaciones': Reservacion.objects.filter(
                usuario_registro=request.user.id, 
                fecha_entrada__date=localdate()
            )[:3],
            'hoy': localdate(),
            'habitaciones_sample': Habitacion.objects.all()[:6],
            'reservas_hoy_count': Reservacion.objects.filter(
                usuario_registro=request.user.id, 
                fecha_entrada__date=localdate()
            ).count(),
            'porcentaje_ocupacion': 65,  # Temporalmente fijo
            'habitaciones_disponibles': Habitacion.objects.filter(disponible=True).count(),
        }
        return render(request, 'myapp/dashboard.html', context)
        
    except Exception as e:
        print(f"Error en dashboard: {e}")
        # Versión de emergencia
        return render(request, 'myapp/dashboard.html', {
            'reservas_total': 0,
            'cantidad_habitaciones': 0,
            'clientes': 0,
            'total_ingresos': 0,
            'reservaciones': [],
            'hoy': localdate(),
            'habitaciones_sample': [],
            'reservas_hoy_count': 0,
            'porcentaje_ocupacion': 0,
            'habitaciones_disponibles': 0,
        })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'✅ Cuenta creada exitosamente para {username}. ¡Bienvenido/a!')
            return redirect('login')
        else:
            # Mostrar el primer error encontrado
            first_error = next(iter(form.errors.values()))[0]
            messages.error(request, first_error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/registro.html', {'form': form})

def custom_logout_view(request):
    try:
        # 1. Cerrar sesión
        logout(request)
        
        # 2. Cerrar conexión a la BD manualmente
        connection.close()
        
        # 3. Redireccionar
        return redirect('home')
        
    except:
        # Si algo falla, asegurarse de cerrar la conexión
        connection.close()
        return redirect('home')

@login_required(login_url='/login/')
def lista_habitaciones(request):
    Habitacion.objects.filter(seleccionada=True).update(seleccionada=False)
    fecha_actual = timezone.now()
    for f in Reservacion.objects.all():
        for h in Habitacion.objects.all():
            #despues de que se acabe la reserva la habitacion pasa a estar disponible
            if h.disponible == False and f.fecha_salida < fecha_actual:
                if f.habitacion == h:
                    h.disponible = True
                    h.save()
        #eliminar reservas 
        if f.fecha_salida< fecha_actual:
            f.delete()
    habitaciones = Habitacion.objects.all()
    habitaciones_disponibles = Habitacion.objects.filter(disponible=True).count()
    habitaciones_ocupadas = Habitacion.objects.filter(disponible=False).count()
    context = {
        'habitaciones': habitaciones,
        'total_habitaciones': Habitacion.objects.count(),
        'habitaciones_disponibles': habitaciones_disponibles,
        'habitaciones_ocupadas': habitaciones_ocupadas,
    }
    return render(request, 'myapp/lista_habitaciones.html', context)

@login_required(login_url='/login/')
def reservacion(request):
    habitaciones = Habitacion.objects.all()
    if request.method == 'POST':
        
        form = ReservacionForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario_registro = request.user
            reserva.save()
            
            # Marcar habitación como no disponible
            reserva.habitacion.disponible = False
            reserva.habitacion.save()
            
            messages.success(request, '✅ Reservación creada exitosamente')
            return redirect('lista_reservaciones')
    else:
        form = ReservacionForm()

    context = {
            'form': form,
            'habitaciones': habitaciones,
            }
    return render(request, 'myapp/reservacion.html', context)

@login_required(login_url='/login/')
def seleccionar_habitacion(request, habitacion_id):
    if request.method == "POST":
        habitacion = get_object_or_404(Habitacion, id=habitacion_id)
        habitacion.seleccionada = True  
        habitacion.save()
        messages.success(request, f'✅ Habitación {habitacion.numero} seleccionada')
    return redirect('reservacion')

@login_required(login_url='/login/')
def lista_reservaciones(request):
    hoy = timezone.now()
    reservas = Reservacion.objects.all()
    total_ingresos = 0

    for reserva in reservas:
        noches = (reserva.fecha_salida.date() - reserva.fecha_entrada.date()).days
        total_ingresos += reserva.habitacion.precio * noches
    
    # Reservaciones activas (check-out en el futuro)
    reservaciones = Reservacion.objects.filter(
        fecha_salida__gte=hoy
    ).select_related('cliente', 'habitacion').order_by('fecha_entrada')
    
    # Opcional: Filtro por fechas desde URL
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            reservaciones = reservaciones.filter(
                fecha_entrada__date__gte=fecha_inicio,
                fecha_salida__date__lte=fecha_fin
            )
        except ValueError:
            messages.error(request, "Formato de fecha incorrecto. Use YYYY-MM-DD")
    
    return render(request, 'myapp/lista_reservaciones.html', {
        'reservaciones': reservaciones,
        'hoy': hoy, #.date()
        'ingresos_totales': total_ingresos,
        'clientes_activos': Cliente.objects.count(),
        'habitaciones_ocupadas': Habitacion.objects.filter(disponible=False).count(),
    })

@login_required(login_url='/login/')
def registrar_cliente(request):
    if request.method == 'POST':
        #se registra los clientes
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cliente')  
    else:
        form = ClienteForm()
    context = {
            'form': form,
            }
    return render(request,'myapp/registrar_cliente.html', context) 

def lista_cliente(request):
    clientes = Cliente.objects.all()  
    context = {
        'clientes': clientes,
    }
    return render(request, 'myapp/lista_clientes.html', context)

@require_POST
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('lista_cliente')

# =============================================
# NUEVAS VISTAS PARA LOS MÓDULOS AGREGADOS
# =============================================

@login_required
def perfil_estudiante(request):
    """
    Vista para el perfil del estudiante
    """
    # Obtener o crear el perfil del usuario
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Calcular estadísticas (puedes adaptar según tus modelos)
    estadisticas = {
        'total_simulaciones': Reservacion.objects.filter(usuario_registro=request.user).count(),
        'promedio_general': 87,    # Ejemplo - puedes calcularlo basado en evaluaciones
        'logros_obtenidos': 5,     # Ejemplo
        'especialidades': 3,       # Ejemplo
        'progreso_general': min(Reservacion.objects.filter(usuario_registro=request.user).count() * 10, 100),
    }
    
    if request.method == 'POST':
        # Procesar actualización del perfil
        return update_profile_data(request, profile)
    
    context = {
        'user': request.user,
        'profile': profile,
        'estadisticas': estadisticas,
    }
    
    return render(request, 'myapp/perfil_estudiante.html', context)

def update_profile_data(request, profile):
    """
    Función auxiliar para actualizar los datos del perfil
    """
    try:
        # Actualizar datos básicos del usuario
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Actualizar perfil extendido
        profile.institution = request.POST.get('institution', 'UTD Francisco Tamayo')
        profile.semester = int(request.POST.get('semester', 1))
        profile.career = request.POST.get('career', 'Turismo')
        profile.specialization = request.POST.get('specialization', 'recepcion')
        
        # Preferencias de notificación
        profile.email_notifications = 'email_notifications' in request.POST
        profile.practice_reminders = 'practice_reminders' in request.POST
        profile.progress_updates = 'progress_updates' in request.POST
        profile.newsletter = 'newsletter' in request.POST
        
        profile.save()
        
        messages.success(request, 'Perfil actualizado correctamente')
        
    except Exception as e:
        messages.error(request, f'Error al actualizar el perfil: {str(e)}')
    
    return redirect('perfil_estudiante')

@login_required
def upload_avatar(request):
    """
    API para subir avatar del usuario
    """
    if request.method == 'POST' and request.FILES.get('avatar'):
        try:
            profile = UserProfile.objects.get(user=request.user)
            avatar_file = request.FILES['avatar']
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if avatar_file.content_type not in allowed_types:
                return JsonResponse({'success': False, 'error': 'Tipo de archivo no permitido'})
            
            # Validar tamaño (máximo 2MB)
            if avatar_file.size > 2 * 1024 * 1024:
                return JsonResponse({'success': False, 'error': 'La imagen no puede ser mayor a 2MB'})
            
            # Guardar el archivo
            file_extension = avatar_file.name.split('.')[-1]
            filename = f"avatar_{request.user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
            
            # Crear directorio si no existe
            avatars_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            os.makedirs(avatars_dir, exist_ok=True)
            
            file_path = os.path.join(avatars_dir, filename)
            
            with open(file_path, 'wb+') as destination:
                for chunk in avatar_file.chunks():
                    destination.write(chunk)
            
            # Actualizar perfil con la nueva ruta del avatar
            profile.avatar = f'avatars/{filename}'
            profile.save()
            
            return JsonResponse({
                'success': True, 
                'avatar_url': profile.avatar.url,
                'message': 'Avatar actualizado correctamente'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def configuracion_sistema(request):
    """
    Vista para la configuración del sistema (solo para administradores)
    """
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Obtener configuración actual del sistema
    settings_obj, created = SystemSettings.objects.get_or_create(id=1)
    
    # Obtener historial de backups
    backup_history = BackupHistory.objects.all().order_by('-created_at')[:5]
    
    # Estadísticas del sistema
    system_stats = {
        'total_estudiantes': UserProfile.objects.count(),
        'simulaciones_hoy': Reservacion.objects.filter(
            fecha_entrada__date=localdate()
        ).count(),
        'total_reservaciones': Reservacion.objects.count(),
        'habitaciones_ocupadas': Habitacion.objects.filter(disponible=False).count(),
    }
    
    if request.method == 'POST':
        return save_system_settings_data(request, settings_obj)
    
    context = {
        'settings': settings_obj,
        'backup_history': backup_history,
        'system_stats': system_stats,
    }
    
    return render(request, 'myapp/configuracion_sistema.html', context)

def save_system_settings_data(request, settings_obj):
    """
    Función auxiliar para guardar configuración del sistema
    """
    try:
        # Configuración general
        settings_obj.institution_name = request.POST.get('institution_name', '')
        settings_obj.institution_slogan = request.POST.get('institution_slogan', '')
        settings_obj.contact_email = request.POST.get('contact_email', '')
        settings_obj.contact_phone = request.POST.get('contact_phone', '')
        
        # Configuración académica
        settings_obj.simulation_duration = int(request.POST.get('simulation_duration', 30))
        settings_obj.max_attempts = int(request.POST.get('max_attempts', 3))
        settings_obj.passing_score = int(request.POST.get('passing_score', 70))
        settings_obj.max_students = int(request.POST.get('max_students', 500))
        
        # Configuración regional
        settings_obj.language = request.POST.get('language', 'es')
        settings_obj.timezone = request.POST.get('timezone', 'America/Caracas')
        settings_obj.date_format = request.POST.get('date_format', 'dd/mm/yyyy')
        settings_obj.currency = request.POST.get('currency', 'VES')
        
        # Apariencia
        settings_obj.theme = request.POST.get('theme', 'default')
        
        # Notificaciones del sistema
        settings_obj.email_notifications = 'system_email_notifications' in request.POST
        settings_obj.maintenance_mode = 'maintenance_mode' in request.POST
        settings_obj.auto_backup = 'auto_backup' in request.POST
        
        settings_obj.save()
        
        messages.success(request, 'Configuración del sistema guardada correctamente')
        
    except Exception as e:
        messages.error(request, f'Error al guardar la configuración: {str(e)}')
    
    return redirect('configuracion_sistema')

@login_required
def save_system_settings(request):
    """
    API para guardar configuración del sistema via AJAX
    """
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'No autorizado'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            settings_obj, created = SystemSettings.objects.get_or_create(id=1)
            
            # Actualizar configuración según los datos recibidos
            for key, value in data.items():
                if hasattr(settings_obj, key):
                    setattr(settings_obj, key, value)
            
            settings_obj.save()
            
            return JsonResponse({'success': True, 'message': 'Configuración guardada'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def backup_system(request):
    """
    API para crear backup del sistema
    """
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'No autorizado'})
    
    if request.method == 'POST':
        try:
            # Crear directorio de backups si no existe
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Nombre del archivo de backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'backup_{timestamp}.zip'
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Simular creación de backup (en producción usarías una librería como zipfile)
            with open(backup_path, 'w') as f:
                f.write(f"Backup creado el {datetime.now()}")
            
            # Registrar en el historial
            BackupHistory.objects.create(
                filename=backup_filename,
                size=os.path.getsize(backup_path),
                created_by=request.user
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Backup creado correctamente',
                'filename': backup_filename,
                'size': os.path.getsize(backup_path)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})