"""Vistas del chatbot: separadas por completo del CRUD de inventario."""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .services.ollama_service import responder


def chat_view(request):
    """Interfaz del chat. GET renderiza; POST (AJAX) responde JSON."""
    if request.method == 'POST':
        pregunta = (request.POST.get('pregunta') or '').strip()
        if not pregunta:
            return JsonResponse({'respuesta': 'Escribe una consulta sobre el inventario.', 'ok': False})
        respuesta, disponible = responder(pregunta)
        # Guarda historial mínimo en sesión
        historial = request.session.get('chat_historial', [])
        historial.append({'pregunta': pregunta, 'respuesta': respuesta})
        request.session['chat_historial'] = historial[-20:]
        return JsonResponse({'respuesta': respuesta, 'ok': disponible})
    return render(request, 'chatbot/chat.html', {
        'historial': request.session.get('chat_historial', []),
    })


@require_POST
def chat_api(request):
    pregunta = (request.POST.get('pregunta') or '').strip()
    if not pregunta:
        return JsonResponse({'respuesta': 'Escribe una consulta sobre el inventario.', 'ok': False})
    respuesta, disponible = responder(pregunta)
    return JsonResponse({'respuesta': respuesta, 'ok': disponible})
