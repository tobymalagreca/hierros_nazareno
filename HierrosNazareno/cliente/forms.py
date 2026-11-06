from django import forms
from .models import Cliente

class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # El campo 'usuario' no se incluye aquí porque se vincula internamente en la vista
        fields = ['telefono', 'direccion', 'ciudad']
        
        labels = {
            'telefono': 'Número de Teléfono',
            'direccion': 'Dirección de Entrega',
            'ciudad': 'Ciudad / Localidad',
        }
        
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500',
                'placeholder': 'Ej: 11 4697-8800'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500',
                'placeholder': 'Calle, Número, Piso/Depto'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500',
                'placeholder': 'Ej: Morón'
            }),
        }

class BusquedaForm(forms.Form):
    # Este es un formulario normal (forms.Form), ideal para filtros o búsquedas
    query = forms.CharField(
        max_length=100,
        required=False, # Permite que el usuario envíe el campo vacío para ver todos los productos
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white text-gray-900 placeholder-gray-400 text-sm rounded-lg pl-10 pr-24 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm',
            'placeholder': 'Buscar por perfil IPN, caños estructurales, chapas trapezoidales...'
        })
    )