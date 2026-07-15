from abc import ABC, abstractmethod
from typing import List
from src.Domain.Entities.plato import Plato

class IPlatoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, id_plato: int) -> Plato:
        """Busca un plato específico por su ID"""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Plato]:
        """Trae la lista de los 14 platos para el combo box/dropdown"""
        pass