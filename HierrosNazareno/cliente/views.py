from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # <-- Importación para las notificaciones
from administrador.models import Producto
from .models import Cliente, Pedido, DetallePedido  # <-- Se agrega Pedido al modelo local
from .forms import PerfilClienteForm, BusquedaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from decimal import Decimal

def catalogo_productos(request):
    """
    Vista de lectura (Read): Búsqueda dinámica de productos.
    """
    # Inicializamos el formulario (vacío o con los datos de la URL)
    form = BusquedaForm(request.GET or None)
    
    # Base del QuerySet: solo productos disponibles
    productos = Producto.objects.filter(disponible=True)
    hay_resultados = True

    # 1. Capturamos el parámetro de búsqueda usando request.GET.get()
    query = request.GET.get('query')

    if query:
        # Filtramos usando el lookup __icontains (insensible a mayúsculas/minúsculas)
        productos = productos.filter(nombre__icontains=query)
        
        # Verificamos si existen resultados con .exists() para optimizar el rendimiento
        # en lugar de evaluar todo el QuerySet o usar len()
        if not productos.exists():
            hay_resultados = False

    context = {
        'form': form,
        'productos': productos,
        'hay_resultados': hay_resultados,
        'query': query
    }
    return render(request, 'cliente/catalogo.html', context)


@login_required(login_url='login')
def confirmar_pedido(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('catalogo')

    # 1. Calcular el total usando la variable correcta
    total_pedido = sum(Decimal(str(item['precio'])) * item['cantidad'] for item in carrito.values())
    
    # 2. Crear el registro vinculando 'usuario' y 'total' (los nuevos nombres del modelo)
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total_pedido
    )
    
    # 3. Crear los Detalles del Pedido
    for producto_id, item in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item['cantidad'],
            precio_unitario=item['precio']
        )
        
        # Descontar el stock
        if producto.stock >= item['cantidad']:
            producto.stock -= item['cantidad']
            producto.save()
            
    # 4. Vaciar el carrito de la sesión
    request.session['carrito'] = {}
    
    # 5. Redirigir a la pantalla de éxito
    return render(request, 'cliente/pedido_exitoso.html', {'pedido': pedido})


def agregar_al_carrito(request, producto_id):
    """Agrega un producto al carrito, leyendo la cantidad enviada por el usuario."""
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})
    id_str = str(producto.id)
    
    # Captura la cantidad del formulario (por defecto 1 si falla)
    cantidad = int(request.POST.get('cantidad', 1)) if request.method == 'POST' else 1

    if id_str in carrito:
        carrito[id_str]['cantidad'] += cantidad
    else:
        carrito[id_str] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': cantidad
        }
    
    request.session['carrito'] = carrito
    messages.success(request, f"{cantidad}x {producto.nombre} agregado al carrito.")
    return redirect('catalogo')

def actualizar_carrito(request, producto_id):
    """Suma o resta cantidades directamente dentro del carrito."""
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        id_str = str(producto_id)
        accion = request.POST.get('accion')
        
        if id_str in carrito:
            if accion == 'sumar':
                carrito[id_str]['cantidad'] += 1
            elif accion == 'restar':
                if carrito[id_str]['cantidad'] > 1:
                    carrito[id_str]['cantidad'] -= 1
                else:
                    del carrito[id_str] # Si resta a 0, lo elimina
        
        request.session['carrito'] = carrito
    return redirect('ver_carrito')

def eliminar_del_carrito(request, producto_id):
    """Elimina por completo un producto del carrito."""
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
        messages.success(request, "Producto eliminado.")
        
    return redirect('ver_carrito')

def ver_carrito(request):
    """
    Lee la sesión y calcula el total para mostrarlo al usuario.
    """
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    
    return render(request, 'cliente/carrito.html', {
        'carrito': carrito,
        'total': total
    })


@login_required
def editar_perfil_cliente(request, id):
    """
    Vista de modificación (Update): Captura ID, obtiene objeto y vincula la instancia.
    Protegida con @login_required.
    """
    # 2. Capturamos el ID y usamos get_object_or_404 para manejar errores 404 elegantemente
    cliente_obj = get_object_or_404(Cliente, id=id)
    
    # Opcional (Buenas prácticas): Validar que el usuario solo edite su propio perfil
    if cliente_obj.usuario != request.user:
        return redirect('catalogo')

    if request.method == 'POST':
        # Vinculamos los datos recibidos (POST) con la instancia existente (instance=cliente_obj)
        form = PerfilClienteForm(request.POST, instance=cliente_obj)
        if form.is_valid():
            form.save()
            return redirect('catalogo')  # Redirigir al éxito
    else:
        # Petición GET: Poblamos el formulario con la instancia de la base de datos
        form = PerfilClienteForm(instance=cliente_obj)

    return render(request, 'cliente/editar_perfil.html', {'form': form})




def registro_cliente(request):
    """Maneja el registro de nuevos usuarios y los loguea automáticamente."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido {user.username}! Tu cuenta ha sido creada.")
            return redirect('catalogo')
    else:
        form = UserCreationForm()
    
    return render(request, 'cliente/registro.html', {'form': form})