"""Las 8 estrategias concretas de reportes de Lucerito."""
from django.db.models import F, Sum

from ..models import Producto
from .base import ReportStrategy


def _producto_a_dict(p):
    return {
        'Código': p.codigo,
        'Nombre': p.nombre,
        'Descripción': p.descripcion,
        'Categoría': p.categoria,
        'Marca': p.marca,
        'Precio': str(p.precio),
        'Cantidad existente': p.cantidad_existente,
        'Stock mínimo': p.stock_minimo,
        'Estado del producto': 'Activo' if p.estado else 'Inactivo',
        'Fecha de registro': p.fecha_registro.strftime('%Y-%m-%d %H:%M') if p.fecha_registro else '',
    }


class ListadoGeneralStrategy(ReportStrategy):
    clave = 'general'
    titulo = 'Listado general de productos activos'
    descripcion = 'Todos los productos con estado activo.'

    def generar(self):
        productos = Producto.objects.filter(estado=True).order_by('nombre')
        datos = [_producto_a_dict(p) for p in productos]
        return {
            'titulo': self.titulo,
            'resumen': f'{len(datos)} productos activos.',
            'datos': datos,
        }


class MasCaroStrategy(ReportStrategy):
    clave = 'mas_caro'
    titulo = 'Producto más caro'
    descripcion = 'El producto activo con mayor precio.'

    def generar(self):
        p = Producto.objects.filter(estado=True).order_by('-precio').first()
        datos = [_producto_a_dict(p)] if p else []
        return {
            'titulo': self.titulo,
            'resumen': f'{p.nombre} (${p.precio})' if p else 'Sin productos.',
            'datos': datos,
        }


class MasBaratoStrategy(ReportStrategy):
    clave = 'mas_barato'
    titulo = 'Producto más barato'
    descripcion = 'El producto activo con menor precio.'

    def generar(self):
        p = Producto.objects.filter(estado=True).order_by('precio').first()
        datos = [_producto_a_dict(p)] if p else []
        return {
            'titulo': self.titulo,
            'resumen': f'{p.nombre} (${p.precio})' if p else 'Sin productos.',
            'datos': datos,
        }


class PocoStockStrategy(ReportStrategy):
    clave = 'poco_stock'
    titulo = 'Productos con pocas existencias'
    descripcion = 'Cantidad existente menor o igual al stock mínimo.'

    def generar(self):
        productos = Producto.objects.filter(
            estado=True, cantidad_existente__lte=F('stock_minimo')
        ).order_by('cantidad_existente')
        datos = [_producto_a_dict(p) for p in productos]
        return {
            'titulo': self.titulo,
            'resumen': f'{len(datos)} productos con poco stock.',
            'datos': datos,
        }


class AgotadosStrategy(ReportStrategy):
    clave = 'agotados'
    titulo = 'Productos agotados'
    descripcion = 'Cantidad existente igual a cero.'

    def generar(self):
        productos = Producto.objects.filter(estado=True, cantidad_existente=0)
        datos = [_producto_a_dict(p) for p in productos]
        return {
            'titulo': self.titulo,
            'resumen': f'{len(datos)} productos agotados.',
            'datos': datos,
        }


class PorCategoriaStrategy(ReportStrategy):
    clave = 'por_categoria'
    titulo = 'Productos por categoría'
    descripcion = 'Agrupados y conteo por categoría.'

    def generar(self):
        productos = Producto.objects.filter(estado=True).order_by('categoria', 'nombre')
        grupos = {}
        for p in productos:
            grupos.setdefault(p.categoria, []).append(_producto_a_dict(p))
        resumen = '; '.join(f'{cat}: {len(items)}' for cat, items in grupos.items()) or 'Sin productos.'
        # Para la tabla se aplana con la categoría incluida
        datos = [item for items in grupos.values() for item in items]
        return {'titulo': self.titulo, 'resumen': resumen, 'datos': datos, 'grupos': grupos}


class ValorTotalStrategy(ReportStrategy):
    clave = 'valor_total'
    titulo = 'Valor total del inventario'
    descripcion = 'Suma de precio por cantidad existente.'

    def generar(self):
        total = Producto.objects.filter(estado=True).aggregate(
            total=Sum(F('precio') * F('cantidad_existente'))
        )['total'] or 0
        n = Producto.objects.filter(estado=True).count()
        return {
            'titulo': self.titulo,
            'resumen': f'Valor total: ${total:.2f} en {n} productos activos.',
            'datos': [{'Valor total del inventario': f'${float(total):.2f}', 'Productos activos': n}],
            'total': float(total),
        }


class MayorCantidadStrategy(ReportStrategy):
    clave = 'mayor_cantidad'
    titulo = 'Productos con mayor cantidad disponible'
    descripcion = 'Top 10 por cantidad existente.'

    def generar(self):
        productos = Producto.objects.filter(estado=True).order_by('-cantidad_existente')[:10]
        datos = [_producto_a_dict(p) for p in productos]
        return {
            'titulo': self.titulo,
            'resumen': 'Top 10 por disponibilidad.',
            'datos': datos,
        }
