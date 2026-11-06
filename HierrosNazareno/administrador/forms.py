from django import forms
from .models import Producto

class CrearProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Excluimos 'fecha_ingreso' porque se asigna automáticamente (auto_now_add=True)
        fields = ['categoria', 'codigo', 'nombre', 'precio', 'stock', 'peso_kg', 'disponible']
        
        labels = {
            'categoria': 'Categoría',
            'codigo': 'Código SKU',
            'nombre': 'Nombre del Producto',
            'precio': 'Precio Unitario ($)',
            'stock': 'Stock Actual',
            'peso_kg': 'Peso Teórico (Kg)',
            'disponible': '¿El producto está activo y visible?',
        }
        
        widgets = {
            'categoria': forms.Select(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500 focus:border-blue-500'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: TB-505020'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: Tubo Estructural Cuadrado 50x50x2.0 mm'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': '42850.00',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Cantidad en barras'
            }),
            'peso_kg': forms.NumberInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md p-2.5 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: 17.7',
                'step': '0.01'
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
            }),
        }