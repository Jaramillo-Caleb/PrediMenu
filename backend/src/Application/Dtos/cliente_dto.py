from dataclasses import dataclass

@dataclass
class ClienteRequestDTO:
    nombre: str
    email: str
    id_restaurante: int

@dataclass
class ClienteResponseDTO:
    id_cliente: int
    nombre: str
    email: str