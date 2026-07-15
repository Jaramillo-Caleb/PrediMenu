from abc import ABC, abstractmethod
from src.Domain.Entities.venta_plato import VentaPlato

class IVentaRepository(ABC):
    @abstractmethod
    def guardar(self, venta: VentaPlato) -> int:
        """Crea el registro de la predicción en la mañana"""
        pass

    @abstractmethod
    def obtener_por_id(self, id_venta: int) -> VentaPlato:
        """Busca un registro de venta para el seguimiento o cierre"""
        pass

    @abstractmethod
    def actualizar(self, venta: VentaPlato) -> bool:
        """Actualiza los datos reales al corte de las 3pm o cierre de noche"""
        pass

    @abstractmethod
    def set_promo_enviada(self, id_venta: int, valor: bool) -> bool:
        """Marca que ya se envió la promoción para esta venta, evita duplicados"""
        pass