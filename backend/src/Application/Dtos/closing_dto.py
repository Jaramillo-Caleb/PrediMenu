from dataclasses import dataclass
from typing import List

@dataclass
class ClosingItemDTO:
    id_venta_plato: int
    cantidad_normal: int
    cantidad_excedente: int
    cantidad_descartada: int

@dataclass
class ClosingRequestDTO:
    items: List[ClosingItemDTO]

@dataclass
class ClosingResponseDTO:
    id_venta_plato: int
    actualizado: bool