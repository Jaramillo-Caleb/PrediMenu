from abc import ABC, abstractmethod
from typing import List
from src.Domain.Entities.cliente import Cliente

class IClienteRepository(ABC):
    @abstractmethod
    def guardar(self, cliente: Cliente) -> int:
        """Registra un cliente nuevo desde el QR"""
        pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Cliente:
        """Evita duplicados si el mismo cliente escanea el QR dos veces"""
        pass

    @abstractmethod
    def obtener_por_restaurante(self, id_restaurante: int) -> List[Cliente]:
        """Lista de destinatarios para el envío de notificaciones"""
        pass