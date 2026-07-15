import jwt
from functools import wraps
from flask import request, jsonify, g

def crear_requiere_token(secret_key):
    def requiere_token(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Token no proporcionado"}), 401

            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, secret_key, algorithms=["HS256"])
                g.usuario = payload  
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expirado, inicia sesión de nuevo"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Token inválido"}), 401

            return f(*args, **kwargs)
        return decorated
    return requiere_token