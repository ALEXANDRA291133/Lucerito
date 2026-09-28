"""Pruebas unitarias: validación de unicidad y reportes de inventario."""
from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from .models import Producto
from .strategies import ReportFactory


def crear_producto(codigo='LAB-001', precio='10.00', cantidad=10, stock=5,
                   categoria='Maquillaje', estado=True):
    return Producto.objects.create(
        codigo=codigo, nombre=f'Producto {codigo}', descripcion='Desc',
        categoria=categoria, marca='Test', precio=Decimal(precio),
        cantidad_existente=cantidad, stock_minimo=stock, estado=estado,
    )


class ProductoValidacionTests(TestCase):
    def test_codigo_unico(self):
        crear_producto(codigo='LAB-001')
        with self.assertRaises(IntegrityError):
            crear_producto(codigo='LAB-001')

    def test_precio_no_negativo_form(self):
        from .forms import ProductoForm
        form = ProductoForm(data={
            'codigo': 'X-1', 'nombre': 'P', 'descripcion': '',
            'categoria': 'Maquillaje', 'marca': 'M', 'precio': -5,
            'cantidad_existente': 1, 'stock_minimo': 1, 'estado': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_cantidad_y_stock_no_negativos_form(self):
        from .forms import ProductoForm
        for campo in ('cantidad_existente', 'stock_minimo'):
            data = {'codigo': f'X-{campo}', 'nombre': 'P', 'descripcion': '',
                    'categoria': 'Maquillaje', 'marca': 'M', 'precio': 5,
                    'cantidad_existente': 1, 'stock_minimo': 1, 'estado': True}
            data[campo] = -1
            form = ProductoForm(data=data)
            self.assertFalse(form.is_valid(), campo)
            self.assertIn(campo, form.errors)

    def test_form_detecta_codigo_duplicado(self):
        from .forms import ProductoForm
        crear_producto(codigo='DUP-1')
        form = ProductoForm(data={
            'codigo': 'DUP-1', 'nombre': 'Otro', 'descripcion': '',
            'categoria': 'Maquillaje', 'marca': 'M', 'precio': 5,
            'cantidad_existente': 1, 'stock_minimo': 1, 'estado': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('codigo', form.errors)


class ReportesTests(TestCase):
    def setUp(self):
        crear_producto('A-1', precio='100.00', cantidad=2, stock=5)   # caro, poco stock
        crear_producto('A-2', precio='5.00', cantidad=0, stock=3)     # barato, agotado
        crear_producto('A-3', precio='20.00', cantidad=50, stock=5)   # mayor cantidad
        crear_producto('A-4', precio='10.00', cantidad=4, stock=2, estado=False)  # inactivo

    def test_listado_general_solo_activos(self):
        r = ReportFactory.get_strategy('general').generar()
        self.assertEqual(len(r['datos']), 3)

    def test_mas_caro_y_mas_barato(self):
        caro = ReportFactory.get_strategy('mas_caro').generar()
        self.assertEqual(caro['datos'][0]['Código'], 'A-1')
        barato = ReportFactory.get_strategy('mas_barato').generar()
        self.assertEqual(barato['datos'][0]['Código'], 'A-2')

    def test_poco_stock_y_agotados(self):
        poco = ReportFactory.get_strategy('poco_stock').generar()
        codigos = {d['Código'] for d in poco['datos']}
        self.assertIn('A-1', codigos)
        self.assertIn('A-2', codigos)
        agot = ReportFactory.get_strategy('agotados').generar()
        self.assertEqual([d['Código'] for d in agot['datos']], ['A-2'])

    def test_valor_total(self):
        r = ReportFactory.get_strategy('valor_total').generar()
        esperado = 100 * 2 + 5 * 0 + 20 * 50
        self.assertAlmostEqual(r['total'], esperado)

    def test_mayor_cantidad(self):
        r = ReportFactory.get_strategy('mayor_cantidad').generar()
        self.assertEqual(r['datos'][0]['Código'], 'A-3')

    def test_por_categoria(self):
        r = ReportFactory.get_strategy('por_categoria').generar()
        self.assertIn('Maquillaje', r['grupos'])

    def test_factory_rechaza_clave_invalida(self):
        with self.assertRaises(ValueError):
            ReportFactory.get_strategy('no_existe')
