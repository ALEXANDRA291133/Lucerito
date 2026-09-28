"""Pruebas del chatbot (servicio Ollama con mocks)."""
from unittest.mock import patch

from django.test import TestCase

from chatbot.services import ollama_service


class OllamaServiceTests(TestCase):
    def test_no_disponible_si_no_hay_conexion(self):
        with patch('chatbot.services.ollama_service.requests.post',
                   side_effect=Exception('caído')):
            respuesta, ok = ollama_service.consultar_ollama('¿Qué hay?', 'ctx')
            self.assertFalse(ok)
            self.assertIn('no está disponible', respuesta)

    def test_seleccionar_estrategias_agotados(self):
        claves = ollama_service.seleccionar_estrategias('¿Qué productos están agotados?')
        self.assertIn('agotados', claves)

    def test_seleccionar_estrategias_valor_total(self):
        claves = ollama_service.seleccionar_estrategias('¿Cuál es el valor total?')
        self.assertIn('valor_total', claves)
