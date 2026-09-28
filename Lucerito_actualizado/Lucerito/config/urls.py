"""URLs principales del proyecto Lucerito."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
    path('chat/', include('chatbot.urls')),
]
