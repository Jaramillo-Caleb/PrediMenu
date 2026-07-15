from src.Application.Services.iplato_service import IPlatoService
from src.Application.Dtos.plato_dto import PlatoResponseDTO

class PlatoService(IPlatoService):
    def __init__(self, plato_repository):
        self.plato_repository = plato_repository

    def listar_todos(self):
        entidades = self.plato_repository.obtener_todos()
        return [PlatoResponseDTO(p.id_plato, p.nombre, float(p.precio)) for p in entidades]