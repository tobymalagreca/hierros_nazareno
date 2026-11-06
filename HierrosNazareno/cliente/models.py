from django.db import models
from django.contrib.auth.models import User
from administrador.models import Producto

class Cliente(models.Model):
    # Relación uno a uno con el modelo User de autenticación de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=250)
    ciudad = models.CharField(max_length=100, default='Morón')
    
    def __str__(self):
        return f"Cliente: {self.usuario.get_full_name() or self.usuario.username}"

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('PENDIENTE', 'Pendiente de pago'),
        ('ARMADO', 'En preparación'),
        ('DESPACHADO', 'En viaje'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='PENDIENTE')

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} ({self.get_estado_display()})"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido #{self.pedido.id})"