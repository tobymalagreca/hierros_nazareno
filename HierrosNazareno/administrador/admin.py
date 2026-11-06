from django.contrib import admin
from .models import Categoria, Producto, ReporteBitacora

# Un registro simple
admin.site.register(Categoria)
admin.site.register(ReporteBitacora)

# Un registro avanzado (para ver más columnas en la lista de productos)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'precio', 'stock', 'disponible')
    list_filter = ('disponible', 'categoria')
    search_fields = ('codigo', 'nombre')