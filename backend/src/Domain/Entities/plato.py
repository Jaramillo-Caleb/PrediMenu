from dataclasses import dataclass

@dataclass
class Plato:
    id_plato: int
    nombre: str
    precio: float
    id_restaurante: int  # FK