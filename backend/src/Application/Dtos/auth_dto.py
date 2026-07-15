from dataclasses import dataclass

@dataclass
class LoginRequestDTO:
    username: str
    password: str

@dataclass
class LoginResponseDTO:
    token: str
    username: str
    id_restaurante: int