from dataclasses import dataclass
from typing import List

@dataclass
class TrackingItemDTO:
    id_venta_plato: int
    cantidad_vendida_actual: int

@dataclass
class TrackingRequestDTO:
    items: List[TrackingItemDTO]

@dataclass
class TrackingResponseDTO:
    id_venta_plato: int
    status: str
    cantidad_restante: int
    descuento_pct: int
    precio_descuento: float
    notificado: bool
    mensaje: str