from abc import ABC, abstractmethod
from typing import List
from src.Application.Dtos.plato_dto import PlatoResponseDTO

class IPlatoService(ABC):
    @abstractmethod
    def listar_todos(self) -> List[PlatoResponseDTO]:
        """Obtiene la lista de los 14 platos base para el dropdown"""
        pass