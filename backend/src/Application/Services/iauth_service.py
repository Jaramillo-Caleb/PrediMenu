from abc import ABC, abstractmethod
from src.Application.Dtos.auth_dto import LoginRequestDTO, LoginResponseDTO

class IAuthService(ABC):
    @abstractmethod
    def login(self, request: LoginRequestDTO) -> LoginResponseDTO:
        """Valida las credenciales del administrador"""
        pass