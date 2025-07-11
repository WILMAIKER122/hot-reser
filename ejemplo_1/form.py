from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Reservacion
from datetime import timedelta

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@dominio.com'}),
        error_messages={
            'invalid': _('⚠️ Por favor, introduce un correo electrónico válido.'),
            'unique': _('⚠️ Este correo electrónico ya está registrado.'),
        }
    )
    
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 8 caracteres'}),
    )
    
    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite tu contraseña'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {k: "" for k in fields}
        labels = {
            'username': _('Nombre de usuario'),
        }
        error_messages = {
            'username': {
                'unique': _('⚠️ Este nombre de usuario ya existe.'),
                'invalid': _('⚠️ El nombre de usuario solo puede contener letras, números y @/./+/-/_.'),
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['username', 'email', 'password1', 'password2']
        missing_fields = []
        
        # Verificar campos vacíos
        for field in required_fields:
            if not cleaned_data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(
                _('⚠️ Todos los campos son obligatorios.')
            )
        
        # Validación de contraseñas
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 
                _('⚠️ Las contraseñas no coinciden. Por favor, inténtalo de nuevo.')
            )
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _('⚠️ Este correo electrónico ya está registrado. Por favor, usa otro.')
            )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if len(password1) < 8:
            raise ValidationError(
                _('⚠️ La contraseña debe tener al menos 8 caracteres.')
            )
        
        if not any(char.isupper() for char in password1):
            raise ValidationError(
                _('⚠️ La contraseña debe contener al menos una letra mayúscula.')
            )
            
        if not any(char.isdigit() for char in password1):
            raise ValidationError(
                _('⚠️ La contraseña debe contener al menos un número.')
            )
            
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password1):
            raise ValidationError(
                _('⚠️ La contraseña debe contener al menos un carácter especial (!@#$%^&*).')
            )
            
        return password1


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario'}),
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña'}),
        label='Contraseña',
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('username') or not cleaned_data.get('password'):
            raise ValidationError(
                _('⚠️ Todos los campos son obligatorios.')
            )
        return cleaned_data


class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida']
        widgets = {
            'fecha_entrada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_salida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

def clean(self):
    cleaned_data = super().clean()
    fecha_entrada = cleaned_data.get("fecha_entrada")
    fecha_salida = cleaned_data.get("fecha_salida")
    
    if fecha_entrada and fecha_salida:
        if fecha_salida <= fecha_entrada:
            raise forms.ValidationError(
                "La fecha de salida debe ser posterior a la de entrada"
            )
        if (fecha_salida - fecha_entrada) > timedelta(days=30):
            raise forms.ValidationError(
                "La estadía máxima es de 30 días"
            )

def clean_habitacion(self):
    habitacion = self.cleaned_data['habitacion']
    if not habitacion.disponible:
        raise forms.ValidationError("Esta habitación no está disponible")
    return habitacion
