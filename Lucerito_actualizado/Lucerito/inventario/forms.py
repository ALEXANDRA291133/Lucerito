"""Formularios del CRUD de productos."""
from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    """Formulario con validaciones de unicidad y valores no negativos."""

    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'descripcion', 'categoria',
            'marca', 'precio', 'cantidad_existente', 'stock_minimo', 'estado',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: LAB-001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Labial mate rosa'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'cantidad_existente': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'marca': 'Marca',
            'precio': 'Precio',
            'cantidad_existente': 'Cantidad existente',
            'stock_minimo': 'Stock mínimo',
            'estado': 'Activo',
        }

    def clean_codigo(self):
        codigo = (self.cleaned_data.get('codigo') or '').strip()
        if not codigo:
            raise forms.ValidationError('El código es obligatorio.')
        qs = Producto.objects.filter(codigo__iexact=codigo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un producto con este código.')
        return codigo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_cantidad_existente(self):
        valor = self.cleaned_data.get('cantidad_existente')
        if valor is not None and valor < 0:
            raise forms.ValidationError('La cantidad existente no puede ser negativa.')
        return valor

    def clean_stock_minimo(self):
        valor = self.cleaned_data.get('stock_minimo')
        if valor is not None and valor < 0:
            raise forms.ValidationError('El stock mínimo no puede ser negativo.')
        return valor
