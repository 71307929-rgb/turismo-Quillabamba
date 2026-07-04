# pedidos/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # INICIO
    path("", views.inicio, name="inicio"),
    path("inicio/", views.inicio, name="inicio"),

    # Rutas Principales
    path("productos/", views.lista_productos, name="lista_productos"),
    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),
    path("pedido/<int:pedido_id>/", views.detalle_pedido, name="detalle_pedido"),
    path("reporte-ventas/", views.reporte_ventas, name="reporte_ventas"),
    
    # Rutas del Carrito
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("agregar/<int:producto_id>/", views.agregar_producto, name="agregar"),
    path("eliminar/<int:producto_id>/", views.eliminar_producto, name="eliminar"),
    path("restar/<int:producto_id>/", views.restar_producto, name="restar"),
    path("limpiar/", views.limpiar_carrito, name="limpiar"),
    path("confirmar/", views.confirmar_pedido, name="confirmar_pedido"),

    # Login y Logout
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
]