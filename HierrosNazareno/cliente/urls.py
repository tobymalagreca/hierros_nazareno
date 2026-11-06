from django.urls import path
from . import views

urlpatterns = [
    # Ruta raíz
    path('', views.catalogo_productos, name='catalogo'),
    
    # Perfil
    path('perfil/editar/<int:id>/', views.editar_perfil_cliente, name='editar_perfil'),

    # Carrito y Pedidos
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_carrito'),
    path('carrito/ver/', views.ver_carrito, name='ver_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
]