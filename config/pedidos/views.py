# pedidos/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .carrito import Carrito
from .models import Producto, Pedido, DetallePedido
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


def inicio(request):
    return render(request, "inicio.html")


# === FUNCIÓN DE LISTA DE PRODUCTOS CON BUSCADOR ===
def lista_productos(request):
    buscar = request.GET.get("buscar")
    productos = Producto.objects.all()

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    return render(
        request,
        "productos/lista.html",
        {
            "productos": productos,
            "buscar": buscar
        }
    )


# === VISTAS PARA EL CONTROL DEL CARRITO ===
def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect(request.META.get("HTTP_REFERER", "lista_productos"))


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("ver_carrito")


def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("ver_carrito")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("ver_carrito")


def ver_carrito(request):
    carrito = request.session.get("carrito", {})
    return render(request, "carrito.html", {"carrito": carrito})


# === VISTAS PARA LOS PEDIDOS Y VALIDACIÓN DE STOCK ===
@login_required
def confirmar_pedido(request):
    carrito_sesion = request.session.get("carrito")
    if not carrito_sesion:
        return redirect("lista_productos")

    try:
        pedido = Pedido.objects.create(usuario=request.user)
    except TypeError:
        try:
            pedido = Pedido.objects.create(user=request.user)
        except TypeError:
            try:
                pedido = Pedido.objects.create(cliente=request.user)
            except TypeError:
                pedido = Pedido.objects.create()
                if hasattr(pedido, 'usuario'):
                    pedido.usuario = request.user
                elif hasattr(pedido, 'user'):
                    pedido.user = request.user
                elif hasattr(pedido, 'cliente'):
                    pedido.cliente = request.user
                pedido.save()

    total = 0

    for key, value in carrito_sesion.items():
        producto = Producto.objects.get(id=key)
        amount = value["cantidad"]

        if producto.stock < amount:
            messages.error(
                request,
                f"No hay suficiente stock para {producto.nombre}. Disponible: {producto.stock}"
            )
            pedido.delete()
            return redirect("ver_carrito")

        subtotal = producto.precio * amount

        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=amount
        )

        producto.stock -= amount
        producto.save()

        total += subtotal

    if hasattr(pedido, 'total'):
        pedido.total = total
        pedido.save()

    request.session["carrito"] = {}
    return redirect("mis_pedidos")


# Vista simple para ver el historial
@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, "pedidos/mis_pedidos.html", {"pedidos": pedidos})


# ===== DETALLE DEL PEDIDO =====
@login_required
def detalle_pedido(request, pedido_id):
    detalles = DetallePedido.objects.filter(
        pedido_id=pedido_id
    )
    return render(
        request,
        "pedidos/detalle.html",
        {"detalles": detalles}
    )


# ===== REPORTE DE VENTAS CORREGIDO SIN CAMPO 'TOTAL' =====
@login_required
def reporte_ventas(request):
    buscar = request.GET.get("buscar")
    pedidos_db = Pedido.objects.all()

    # Filtro de búsqueda por nombre de usuario
    if buscar:
        pedidos_db = pedidos_db.filter(usuario__username__icontains=buscar)

    pedidos_con_total = []
    total_general = 0

    # Iteramos para calcular el total de cada pedido usando sus detalles relacionales
    for pedido in pedidos_db:
        detalles = DetallePedido.objects.filter(pedido=pedido)
        total_pedido = sum(d.cantidad * d.producto.precio for d in detalles)
        
        # Guardamos dinámicamente el valor calculado en el objeto
        pedido.total_calculado = total_pedido
        
        pedidos_con_total.append(pedido)
        total_general += total_pedido

    cantidad_pedidos = len(pedidos_con_total)

    return render(
        request,
        "pedidos/reporte_ventas.html",
        {
            "pedidos": pedidos_con_total,
            "cantidad_pedidos": cantidad_pedidos,
            "total_general": total_general,
            "buscar": buscar
        }
    )