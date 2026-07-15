from abc import ABC, abstractmethod
from src.Domain.Entities.usuario import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    def obtener_por_username(self, username: str) -> Usuario:
        """Busca un usuario por su username para validar el login"""
        pass