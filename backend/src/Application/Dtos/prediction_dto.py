from dataclasses import dataclass
from typing import List

@dataclass
class PredictionRequestDTO:
    id_platos: list[int]
    clima: int # 1=Soleado, 2=Lluvioso, 3=Nublado         
    es_festivo: bool

@dataclass
class PredictionResponseDTO:
    id_venta_plato: int
    id_plato: int
    nombre_plato: str
    cantidad_predicha: int