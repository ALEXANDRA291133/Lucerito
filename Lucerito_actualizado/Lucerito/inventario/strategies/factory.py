"""Factory: crea y registra las estrategias de reporte (patrón Factory)."""
from .report_strategies import (
    AgotadosStrategy,
    ListadoGeneralStrategy,
    MasBaratoStrategy,
    MasCaroStrategy,
    MayorCantidadStrategy,
    PocoStockStrategy,
    PorCategoriaStrategy,
    ValorTotalStrategy,
)


class ReportFactory:
    """Fábrica de estrategias. Punto único de creación para CRUD y chatbot."""

    _registro = {
        ListadoGeneralStrategy.clave: ListadoGeneralStrategy,
        MasCaroStrategy.clave: MasCaroStrategy,
        MasBaratoStrategy.clave: MasBaratoStrategy,
        PocoStockStrategy.clave: PocoStockStrategy,
        AgotadosStrategy.clave: AgotadosStrategy,
        PorCategoriaStrategy.clave: PorCategoriaStrategy,
        ValorTotalStrategy.clave: ValorTotalStrategy,
        MayorCantidadStrategy.clave: MayorCantidadStrategy,
    }

    @classmethod
    def get_strategy(cls, clave):
        """Devuelve una instancia de la estrategia o lanza ValueError."""
        try:
            return cls._registro[clave]()
        except KeyError as exc:
            raise ValueError(f'Reporte desconocido: {clave}') from exc

    @classmethod
    def claves(cls):
        return list(cls._registro.keys())

    @classmethod
    def opciones(cls):
        """Lista de (clave, título, descripción) para la interfaz."""
        return [
            (clave, klass.titulo, klass.descripcion)
            for clave, klass in cls._registro.items()
        ]


REPORTES_DISPONIBLES = ReportFactory.claves()
