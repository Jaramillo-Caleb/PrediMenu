from abc import ABC, abstractmethod
from typing import List
from src.Application.Dtos.prediction_dto import PredictionRequestDTO, PredictionResponseDTO

class IPredictionService(ABC):
    @abstractmethod
    def generar_prediccion(self, request: PredictionRequestDTO) -> List[PredictionResponseDTO]:
        """Toma el clima y plato, consulta el modelo .joblib por cada uno y guarda en DB"""
        pass