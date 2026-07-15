from dataclasses import dataclass

@dataclass
class PlatoResponseDTO:
    id_plato: int
    nombre: str
    precio: float