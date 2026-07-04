from django.db import models
from django.contrib.auth.models import User

# 1. Nueva clase Categoría (Debe ir arriba para que Producto la reconozca)
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# 2. Modelo Producto modificado
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    activo = models.BooleanField(default=True)
    # Nueva relación con Categoría:
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

# 3. Modelo Pedido modificado
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Modificamos esta línea para usar la tabla intermedia 'DetallePedido'
    productos = models.ManyToManyField(Producto, through='DetallePedido')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

# 4. Nuevo Modelo Intermedio para guardar las cantidades
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"