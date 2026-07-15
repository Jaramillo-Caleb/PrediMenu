from src.Application.Services.icliente_service import IClienteService
from src.Application.Dtos.cliente_dto import ClienteResponseDTO
from src.Domain.Entities.cliente import Cliente

class ClienteService(IClienteService):
    def __init__(self, cliente_repository):
        self.cliente_repository = cliente_repository

    def registrar(self, request):
        existente = self.cliente_repository.obtener_por_email(request.email)
        if existente:
            return ClienteResponseDTO(existente.id_cliente, existente.nombre, existente.email)

        nuevo_cliente = Cliente(
            id_cliente=None,
            nombre=request.nombre,
            email=request.email,
            id_restaurante=request.id_restaurante
        )
        id_generado = self.cliente_repository.guardar(nuevo_cliente)
        return ClienteResponseDTO(id_generado, request.nombre, request.email)