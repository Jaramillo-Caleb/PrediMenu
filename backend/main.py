import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from src.Infrastructure.Database.models import db

from src.Infrastructure.Repositories.plato_repository import PlatoRepository
from src.Infrastructure.Repositories.venta_repository import VentaRepository
from src.Infrastructure.Repositories.usuario_repository import UsuarioRepository
from src.Infrastructure.Repositories.cliente_repository import ClienteRepository
from src.Infrastructure.Services.auth_service import AuthService
from src.Infrastructure.Services.plato_service import PlatoService
from src.Infrastructure.Services.prediction_service import PredictionService
from src.Infrastructure.Services.tracking_service import TrackingService
from src.Infrastructure.Services.cliente_service import ClienteService
from src.Infrastructure.Services.email_service import EmailService

from src.Api.Routes.routes import create_routes

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/predi_menu'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

    secret_key = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    mail = Mail(app)

    plato_repo = PlatoRepository()
    venta_repo = VentaRepository()
    usuario_repo = UsuarioRepository()
    cliente_repo = ClienteRepository()

    auth_service = AuthService(usuario_repo, secret_key)
    plato_service = PlatoService(plato_repo)
    prediction_service = PredictionService(plato_repo, venta_repo)
    cliente_service = ClienteService(cliente_repo)
    email_service = EmailService(mail)
    tracking_service = TrackingService(venta_repo, plato_repo, cliente_repo, email_service)

    app.register_blueprint(
        create_routes(auth_service, plato_service, prediction_service, tracking_service, cliente_service, secret_key),
        url_prefix='/api'
    )

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)