"""Interfaz base del patrón Strategy para reportes."""
from abc import ABC, abstractmethod


class ReportStrategy(ABC):
    """Contrato que cumple toda estrategia de reporte/procesamiento."""

    #: clave única usada en URLs, factory y chatbot
    clave = ''
    #: título legible para la interfaz
    titulo = ''
    #: descripción corta para la interfaz
    descripcion = ''

    @abstractmethod
    def generar(self):
        """Ejecuta la consulta y devuelve un dict con `titulo`, `resumen` y `datos`."""
        raise NotImplementedError

    def como_texto(self):
        """Representación en texto plano para inyectar como contexto al chatbot.

        Reutiliza EXACTAMENTE la misma estrategia del backend (requisito).
        """
        resultado = self.generar()
        lineas = [f"Reporte: {resultado.get('titulo', self.titulo)}"]
        resumen = resultado.get('resumen')
        if resumen:
            lineas.append(f"Resumen: {resumen}")
        datos = resultado.get('datos')
        if isinstance(datos, list):
            for item in datos[:50]:  # tope para no saturar el contexto
                if isinstance(item, dict):
                    lineas.append(' | '.join(f'{k}: {v}' for k, v in item.items()))
                else:
                    lineas.append(str(item))
        elif datos is not None:
            lineas.append(str(datos))
        return '\n'.join(lineas)
