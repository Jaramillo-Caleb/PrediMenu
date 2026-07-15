from flask_mail import Message
from src.Application.Services.iemail_service import IEmailService

class EmailService(IEmailService):
    def __init__(self, mail):
        self.mail = mail

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        try:
            msg = Message(subject=asunto, recipients=[destinatario], body=cuerpo)
            self.mail.send(msg)
            return True
        except Exception as e:
            print(f"Error enviando correo a {destinatario}: {e}")
            return False