import jwt
from datetime import datetime, timedelta, timezone
from src.Application.Services.iauth_service import IAuthService
from src.Application.Dtos.auth_dto import LoginResponseDTO

class AuthService(IAuthService):
    def __init__(self, usuario_repository, secret_key):
        self.usuario_repository = usuario_repository
        self.secret_key = secret_key

    def login(self, request):
        usuario = self.usuario_repository.obtener_por_username(request.username)

        if not usuario:
            return None
        if usuario.password != request.password:
            return None

        payload = {
            "username": usuario.username,
            "id_restaurante": usuario.id_restaurante,
            "exp": datetime.now(timezone.utc) + timedelta(hours=8)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")

        return LoginResponseDTO(
            token=token,
            username=usuario.username,
            id_restaurante=usuario.id_restaurante
        )