from django.contrib import admin
from .models import Cliente, Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio_unitario']

# Este decorador ya registra el modelo Pedido, no hace falta llamarlo de nuevo abajo
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_creacion', 'estado', 'total']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['usuario__username']
    inlines = [DetallePedidoInline]

admin.site.register(Cliente)