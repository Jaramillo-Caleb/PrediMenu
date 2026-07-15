from dataclasses import dataclass
from datetime import date

@dataclass
class VentaPlato:
    id_venta_plato: int
    fecha: date
    cantidad_predicha: int   
    cantidad_descartada: int
    cantidad_excedente: int
    cantidad_normal: int
    id_plato: int        
    promo_enviada: bool = False