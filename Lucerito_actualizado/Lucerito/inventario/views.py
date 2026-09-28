"""Vistas CRUD + reportes del inventario Lucerito."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto
from .strategies import ReportFactory


def producto_list(request):
    """Lista solo productos activos, con buscador por nombre/código/categoría."""
    q = (request.GET.get('q') or '').strip()
    categoria = (request.GET.get('categoria') or '').strip()
    productos = Producto.objects.filter(estado=True)
    if q:
        productos = _filtrar_busqueda(productos, q)
    if categoria:
        productos = productos.filter(categoria=categoria)
    contexto = {
        'productos': productos.order_by('nombre'),
        'q': q,
        'categoria_actual': categoria,
        'categorias': [c[0] for c in Producto.CATEGORIAS],
    }
    return render(request, 'inventario/producto_list.html', contexto)


def _filtrar_busqueda(qs, texto):
    from django.db.models import Q
    return qs.filter(
        Q(nombre__icontains=texto) | Q(codigo__icontains=texto)
        | Q(marca__icontains=texto) | Q(categoria__icontains=texto)
    )


def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'inventario/producto_detail.html', {'producto': producto})


def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('producto_list')
        messages.error(request, 'No se pudo crear el producto. Revisa los errores.')
    else:
        form = ProductoForm()
    return render(request, 'inventario/producto_form.html', {'form': form, 'accion': 'Crear'})


def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('producto_list')
        messages.error(request, 'No se pudo actualizar el producto. Revisa los errores.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/producto_form.html', {'form': form, 'accion': 'Editar'})


def producto_delete(request, pk):
    """Borrado lógico: marca estado=False."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.estado = False
        producto.save(update_fields=['estado'])
        messages.success(request, f'Producto "{producto.nombre}" desactivado (borrado lógico).')
        return redirect('producto_list')
    return render(request, 'inventario/producto_confirm_delete.html', {'producto': producto})


def reportes(request):
    """Vista de reportes: usa ReportFactory (Strategy + Factory)."""
    clave = request.GET.get('tipo', 'general')
    opciones = ReportFactory.opciones()
    try:
        estrategia = ReportFactory.get_strategy(clave)
        resultado = estrategia.generar()
    except ValueError:
        messages.error(request, 'Reporte no válido.')
        return redirect('/reportes/?tipo=general')
    contexto = {
        'opciones': opciones,
        'clave_actual': clave,
        'resultado': resultado,
    }
    return render(request, 'inventario/reportes.html', contexto)
