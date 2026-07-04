from django.contrib import admin
from .models import Producto, Pedido, DetallePedido, Categoria

admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Categoria)


