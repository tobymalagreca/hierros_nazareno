from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Producto
from .forms import CrearProductoForm  # Importamos tu formulario exacto
from cliente.models import Pedido, Producto


# Validación: Solo usuarios logueados que sean "staff" pueden entrar
def es_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(es_staff, login_url='login')
def dashboard(request):
    productos = Producto.objects.all()
    # Traemos los pedidos ordenados del más nuevo al más viejo
    pedidos = Pedido.objects.all().order_by('-fecha_creacion') 
    
    return render(request, 'administrador/dashboard.html', {
        'productos': productos,
        'pedidos': pedidos
    })

@user_passes_test(es_staff, login_url='login')
def crear_producto(request):
    """CREATE: Alta de nuevo producto."""
    if request.method == 'POST':
        form = CrearProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('dashboard_admin')
    else:
        form = CrearProductoForm()
    
    return render(request, 'administrador/formulario_producto.html', {'form': form, 'accion': 'Crear Nuevo'})

@user_passes_test(es_staff, login_url='login')
def editar_producto(request, id):
    """UPDATE: Modifica un producto usando instance."""
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = CrearProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('dashboard_admin')
    else:
        # Precarga los datos actuales en el formulario
        form = CrearProductoForm(instance=producto)
        
    return render(request, 'administrador/formulario_producto.html', {'form': form, 'accion': 'Editar'})

@user_passes_test(es_staff, login_url='login')
def eliminar_producto(request, id):
    """DELETE: Eliminación segura en dos pasos (GET para aviso, POST para borrar)."""
    producto = get_object_or_404(Producto, id=id)
    
    # Paso 2: POST confirma y elimina
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"El producto '{nombre}' ha sido eliminado del sistema.")
        return redirect('dashboard_admin')
        
    # Paso 1: GET muestra pantalla de advertencia
    return render(request, 'administrador/eliminar_producto.html', {'producto': producto})