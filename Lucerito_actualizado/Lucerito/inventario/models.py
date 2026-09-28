"""Modelo Producto de la tienda de belleza Lucerito."""
from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    """Producto del inventario con borrado lógico (estado)."""

    CATEGORIAS = [
        ('Maquillaje', 'Maquillaje'),
        ('Cuidado facial', 'Cuidado facial'),
        ('Cuidado capilar', 'Cuidado capilar'),
        ('Cuidado corporal', 'Cuidado corporal'),
        ('Perfumería', 'Perfumería'),
        ('Uñas', 'Uñas'),
        ('Accesorios de belleza', 'Accesorios de belleza'),
    ]

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=30, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=120, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    categoria = models.CharField(max_length=30, choices=CATEGORIAS, verbose_name='Categoría')
    marca = models.CharField(max_length=80, blank=True, verbose_name='Marca')
    precio = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)], verbose_name='Precio',
    )
    cantidad_existente = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name='Cantidad existente',
    )
    stock_minimo = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name='Stock mínimo',
    )
    estado = models.BooleanField(default=True, verbose_name='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'

    @property
    def valor_total(self):
        """Valor del stock de este producto (precio * cantidad)."""
        return self.precio * self.cantidad_existente

    @property
    def tiene_poco_stock(self):
        return self.cantidad_existente <= self.stock_minimo

    @property
    def esta_agotado(self):
        return self.cantidad_existente == 0
