from flask import Blueprint, request, jsonify
from dataclasses import asdict
from src.Application.Dtos.auth_dto import LoginRequestDTO
from src.Application.Dtos.prediction_dto import PredictionRequestDTO
from src.Application.Dtos.tracking_dto import TrackingRequestDTO, TrackingItemDTO
from src.Application.Dtos.notification_dto import NotificationRequestDTO
from src.Application.Dtos.closing_dto import ClosingRequestDTO, ClosingItemDTO
from src.Application.Dtos.cliente_dto import ClienteRequestDTO
from src.Api.Middleware.auth_middleware import crear_requiere_token

def create_routes(auth_service, plato_service, prediction_service, tracking_service, cliente_service, secret_key):
    api_bp = Blueprint('api', __name__)
    requiere_token = crear_requiere_token(secret_key)

    @api_bp.route('/auth/login', methods=['POST'])
    def login():
        data = request.json
        if not data:
            return jsonify({"error": "Body vacío o no es JSON"}), 400
        try:
            dto = LoginRequestDTO(**data)
        except TypeError as e:
            return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400

        result = auth_service.login(dto)
        if not result:
            return jsonify({"error": "Credenciales inválidas"}), 401
        return jsonify(asdict(result)), 200

    @api_bp.route('/platos', methods=['GET'])
    @requiere_token
    def listar_platos():
        try:
            result = plato_service.listar_todos()
            return jsonify([asdict(p) for p in result]), 200
        except Exception as e:
            return jsonify({"error": f"Error al listar platos: {str(e)}"}), 500

    @api_bp.route('/prediccion/generar', methods=['POST'])
    @requiere_token
    def generar_prediccion():
        data = request.json
        if not data:
            return jsonify({"error": "Body vacío o no es JSON"}), 400
        try:
            dto = PredictionRequestDTO(**data)
        except TypeError as e:
            return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400
        try:
            resultado = prediction_service.generar_prediccion(dto)
            return jsonify([asdict(r) for r in resultado]), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Error al generar predicción: {str(e)}"}), 500

    @api_bp.route('/seguimiento/verificar', methods=['POST'])
    @requiere_token
    def verificar_riesgo():
        data = request.json
        if not data or 'items' not in data:
            return jsonify({"error": "Body vacío o falta 'items'"}), 400
        try:
            items = [TrackingItemDTO(**item) for item in data['items']]
            dto = TrackingRequestDTO(items=items)
        except TypeError as e:
            return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400

        resultado = tracking_service.verificar_riesgo(dto)
        return jsonify([asdict(r) for r in resultado]), 200

    @api_bp.route('/notificaciones/disparar', methods=['POST'])
    @requiere_token
    def notificar():
        data = request.json
        if not data:
            return jsonify({"error": "Body vacío o no es JSON"}), 400
        try:
            dto = NotificationRequestDTO(**data)
        except TypeError as e:
            return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400

        success = tracking_service.enviar_notificacion(dto)
        return jsonify({"enviado": success}), 200

    @api_bp.route('/ventas/cierre', methods=['PUT'])
    @requiere_token
    def cerrar():
        data = request.json
        if not data or 'items' not in data:
            return jsonify({"error": "Body vacío o falta 'items'"}), 400
        try:
            items = [ClosingItemDTO(**item) for item in data['items']]
            dto = ClosingRequestDTO(items=items)
        except TypeError as e:
            return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400

        resultado = tracking_service.cerrar_jornada(dto)
        return jsonify([asdict(r) for r in resultado]), 200

    @api_bp.route('/clientes/registrar', methods=['POST'])
    def registrar_cliente():
        data = request.json
        if not data:
            return jsonify({"error": "Body vacío o no es JSON"}), 400
        try:
            dto = ClienteRequestDTO(**data)
        except TypeError as e:
            return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400
        try:
            resultado = cliente_service.registrar(dto)
            return jsonify(asdict(resultado)), 201
        except Exception as e:
            return jsonify({"error": f"Error al registrar cliente: {str(e)}"}), 500

    return api_bp