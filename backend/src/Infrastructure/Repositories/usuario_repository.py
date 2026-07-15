from src.Application.Repositories.iusuario_repository import IUsuarioRepository
from src.Infrastructure.Database.models import UsuarioModel
from src.Domain.Entities.usuario import Usuario

class UsuarioRepository(IUsuarioRepository):
    def obtener_por_username(self, username: str) -> Usuario:
        model = UsuarioModel.query.filter_by(username=username).first()

        if not model:
            return None

        return Usuario(
            id_usuario=model.id_usuario,
            username=model.username,
            password=model.password,
            id_restaurante=model.id_restaurante
        )