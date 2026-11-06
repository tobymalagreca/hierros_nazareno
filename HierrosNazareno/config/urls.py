from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from cliente import views as cliente_views

urlpatterns = [
    # Panel nativo de Django
    path('admin/', admin.site.urls),
    
    # Autenticación global
    path('registro/', cliente_views.registro_cliente, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='cliente/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='catalogo'), name='logout'),
    
    # Conexión con las aplicaciones
    path('gestion/', include('administrador.urls')),
    path('', include('cliente.urls')),
]