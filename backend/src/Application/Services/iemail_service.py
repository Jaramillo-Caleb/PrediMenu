from abc import ABC, abstractmethod

class IEmailService(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        """Envía un correo real. Devuelve True/False según el resultado"""
        pass