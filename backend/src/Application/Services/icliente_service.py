from abc import ABC, abstractmethod
from src.Application.Dtos.cliente_dto import ClienteRequestDTO, ClienteResponseDTO

class IClienteService(ABC):
    @abstractmethod
    def registrar(self, request: ClienteRequestDTO) -> ClienteResponseDTO:
        pass