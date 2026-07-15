from dataclasses import dataclass

@dataclass
class NotificationRequestDTO:
    id_venta_plato: int
    tipo_notificacion: str 