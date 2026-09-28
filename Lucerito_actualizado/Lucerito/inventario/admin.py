from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'marca', 'precio', 'cantidad_existente', 'estado')
    list_filter = ('categoria', 'estado')
    search_fields = ('codigo', 'nombre', 'marca')
