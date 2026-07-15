from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Boolean

db = SQLAlchemy()

class RestauranteModel(db.Model):
    __tablename__ = 'restaurante'
    id_restaurante = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)

class UsuarioModel(db.Model):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    id_restaurante = Column(Integer, ForeignKey('restaurante.id_restaurante'), nullable=False)

class PlatoModel(db.Model):
    __tablename__ = 'plato'
    id_plato = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    id_restaurante = Column(Integer, ForeignKey('restaurante.id_restaurante'), nullable=False)

class VentaPlatoModel(db.Model):
    __tablename__ = 'venta_plato'
    id_venta_plato = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    cantidad_predicha = Column(Integer, nullable=False)
    cantidad_descartada = Column(Integer, default=0)
    cantidad_excedente = Column(Integer, default=0)
    cantidad_normal = Column(Integer, default=0)
    id_plato = Column(Integer, ForeignKey('plato.id_plato'), nullable=False)
    promo_enviada = Column(Boolean, nullable=False, default=False)

class ClienteModel(db.Model):
    __tablename__ = 'cliente'
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    id_restaurante = Column(Integer, ForeignKey('restaurante.id_restaurante'), nullable=False)