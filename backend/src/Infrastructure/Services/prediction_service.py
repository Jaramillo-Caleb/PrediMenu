import joblib
import pandas as pd
from datetime import date, datetime
from typing import List
from src.Application.Services.iprediction_service import IPredictionService
from src.Application.Dtos.prediction_dto import PredictionResponseDTO
from src.Domain.Entities.venta_plato import VentaPlato

WEATHER_MAP = {
    1: 'Sunny',
    2: 'Rainy',
    3: 'Cloudy'
}

class PredictionService(IPredictionService):
    def __init__(self, plato_repository, venta_repository):
        self.plato_repository = plato_repository
        self.venta_repository = venta_repository
        self.model = joblib.load('models/modelo_predimenu.joblib')
        self.encoders = joblib.load('models/encoders_predimenu.joblib')

    def generar_prediccion(self, request) -> List[PredictionResponseDTO]:
        clima_encoded = WEATHER_MAP.get(request.clima)
        if clima_encoded is None:
            raise ValueError(f"Código de clima inválido: {request.clima}. Use 1=Soleado, 2=Lluvioso, 3=Nublado")

        ahora = datetime.now()
        resultados = []

        for id_plato in request.id_platos:
            plato = self.plato_repository.obtener_por_id(id_plato)
            if not plato:
                continue  

            input_df = pd.DataFrame([{
                'restaurant_id': plato.id_restaurante,
                'restaurant_type': self.encoders['restaurant_type'].transform(['Casual Dining'])[0],
                'menu_item_name': self.encoders['menu_item_name'].transform([plato.nombre])[0],
                'meal_type': self.encoders['meal_type'].transform(['Lunch'])[0],
                'weather_condition': self.encoders['weather_condition'].transform([clima_encoded])[0],
                'has_promotion': 0,
                'special_event': int(request.es_festivo),
                'mes': ahora.month,
                'dia_semana': ahora.weekday(),
                'es_fin_de_semana': 1 if ahora.weekday() >= 5 else 0
            }])

            cantidad = int(self.model.predict(input_df)[0])

            nueva_venta = VentaPlato(
                id_venta_plato=None,
                fecha=date.today(),
                cantidad_predicha=cantidad,
                id_plato=id_plato,
                cantidad_normal=0,
                cantidad_excedente=0,
                cantidad_descartada=0
            )
            id_generado = self.venta_repository.guardar(nueva_venta)

            resultados.append(PredictionResponseDTO(id_generado, id_plato, plato.nombre, cantidad))

        return resultados