"""URLs de la app inventario (CRUD + reportes)."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.producto_list, name='producto_list'),
    path('producto/nuevo/', views.producto_create, name='producto_create'),
    path('producto/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('producto/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('producto/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
    path('reportes/', views.reportes, name='reportes'),
]
