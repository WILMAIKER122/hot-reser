from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import CustomUserCreationForm, LoginForm
from .models import Cliente, Habitacion, Reservacion
from .form_reser import ClienteForm, ReservacionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import connection
from datetime import datetime, timedelta

def index(request):
    show_warning = request.session.pop('show_logout_warning', False)
    return render(request, 'index.html', {'show_warning': show_warning})

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
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

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
    return render(request, 'registro.html', {'form': form})

def custom_logout_view(request):
    try:
        # 1. Cerrar sesión
        logout(request)
        
        # 2. Mostrar mensaje (sin tocar la BD)
        messages.warning(request, 'Tu sesión finalizó exitosamente. ¡Vuelve pronto!')
        
        # 3. Cerrar conexión a la BD manualmente
        connection.close()
        
        # 4. Redireccionar
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
    return render(request, 'lista_habitaciones.html', {'habitaciones': habitaciones})

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
    #{'form': form}
    return render(request, 'reservacion.html', context)

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
    
    return render(request, 'lista_reservaciones.html', {
        'reservaciones': reservaciones,
        'hoy': hoy, #.date()
    })

#@login_required(login_url='/login/')
def registrar_cliente(request):
    if request.method == 'POST':
        #se registra los clientes
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservación realizada correctamente.')
            return redirect('home')  
    else:
        form = ClienteForm()
    context = {
            'form': form,
            }
    return render(request,'registrar_cliente.html', context) 