from dataclasses import dataclass

@dataclass
class Usuario:
    id_usuario: int
    username: str
    password: str
    id_restaurante: int  