from typing import List
from src.Application.Repositories.icliente_repository import IClienteRepository
from src.Infrastructure.Database.models import db, ClienteModel
from src.Domain.Entities.cliente import Cliente

class ClienteRepository(IClienteRepository):
    def guardar(self, cliente: Cliente) -> int:
        nuevo = ClienteModel(
            nombre=cliente.nombre,
            email=cliente.email,
            id_restaurante=cliente.id_restaurante
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo.id_cliente

    def obtener_por_email(self, email: str) -> Cliente:
        model = ClienteModel.query.filter_by(email=email).first()
        if not model:
            return None
        return Cliente(
            id_cliente=model.id_cliente,
            nombre=model.nombre,
            email=model.email,
            id_restaurante=model.id_restaurante
        )

    def obtener_por_restaurante(self, id_restaurante: int) -> List[Cliente]:
        models = ClienteModel.query.filter_by(id_restaurante=id_restaurante).all()
        return [
            Cliente(
                id_cliente=m.id_cliente,
                nombre=m.nombre,
                email=m.email,
                id_restaurante=m.id_restaurante
            ) for m in models
        ]