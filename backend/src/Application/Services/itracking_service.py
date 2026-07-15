from abc import ABC, abstractmethod
from typing import List
from src.Application.Dtos.tracking_dto import TrackingRequestDTO, TrackingResponseDTO
from src.Application.Dtos.notification_dto import NotificationRequestDTO
from src.Application.Dtos.closing_dto import ClosingRequestDTO, ClosingResponseDTO

class ITrackingService(ABC):
    @abstractmethod
    def verificar_riesgo(self, request: TrackingRequestDTO) -> List[TrackingResponseDTO]:
        """Lógica de las 3:00 PM: Compara cantidad predicha vs actual"""
        pass

    @abstractmethod
    def enviar_notificacion(self, request: NotificationRequestDTO) -> bool:
        """Dispara correos de oferta o aviso de Sold Out"""
        pass

    @abstractmethod
    def cerrar_jornada(self, request: ClosingRequestDTO) -> List[ClosingResponseDTO]:
        """Lógica de la noche: Actualiza totales finales en la DB"""
        pass