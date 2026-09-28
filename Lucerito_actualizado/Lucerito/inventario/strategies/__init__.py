"""Paquete de estrategias de reportes (patrón Strategy + Factory)."""
from .factory import REPORTES_DISPONIBLES, ReportFactory
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

__all__ = [
    'ReportFactory', 'REPORTES_DISPONIBLES',
    'ListadoGeneralStrategy', 'MasCaroStrategy', 'MasBaratoStrategy',
    'PocoStockStrategy', 'AgotadosStrategy', 'PorCategoriaStrategy',
    'ValorTotalStrategy', 'MayorCantidadStrategy',
]
