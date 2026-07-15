from typing import List
from src.Application.Repositories.iplato_repository import IPlatoRepository
from src.Infrastructure.Database.models import PlatoModel
from src.Domain.Entities.plato import Plato

class PlatoRepository(IPlatoRepository):
    
    def obtener_por_id(self, id_plato: int) -> Plato:
        model = PlatoModel.query.get(id_plato)
        
        if not model:
            return None

        return Plato(
            id_plato=model.id_plato,
            nombre=model.nombre,
            precio=float(model.precio),
            id_restaurante=model.id_restaurante
        )

    def obtener_todos(self) -> List[Plato]:
        models = PlatoModel.query.all()
        
        return [
            Plato(
                id_plato=m.id_plato,
                nombre=m.nombre,
                precio=float(m.precio),
                id_restaurante=m.id_restaurante
            ) for m in models
        ]