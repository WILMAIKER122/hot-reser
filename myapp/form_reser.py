from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Reservacion, Cliente, Habitacion

class ClienteForm(forms.ModelForm):  # Cambiado a ClienteForm
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'email']
        
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'cedula': 'Cédula',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico'
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Ingrese su cédula'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese su teléfono'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su email'})
        }
        
        error_messages = {
            'nombre': {
                'required': _('El nombre es obligatorio'),
            },
            'apellido': {
                'required': _('El apellido es obligatorio'),
            },
            'cedula': {
                'required': _('La cédula es obligatoria'),
                'unique': _('Esta cédula ya está registrada')
            }
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if len(cedula) < 6:
            raise ValidationError(
                _('La cédula debe tener al menos 6 caracteres')
            )
        return cedula


class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        exclude = ('codigo_reserva', 'usuario_registro', 'created_at')
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida']
        widgets = {
            'fecha_entrada': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'fecha_salida': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los querysets si es necesario
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['habitacion'].queryset = Habitacion.objects.filter(disponible=True)