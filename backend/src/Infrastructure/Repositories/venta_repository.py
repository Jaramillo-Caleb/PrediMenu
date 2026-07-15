from src.Application.Repositories.iventa_repository import IVentaRepository
from src.Infrastructure.Database.models import db, VentaPlatoModel
from src.Domain.Entities.venta_plato import VentaPlato

class VentaRepository(IVentaRepository):

    def guardar(self, venta: VentaPlato) -> int:
        nuevo_registro = VentaPlatoModel(
            fecha=venta.fecha,
            cantidad_predicha=venta.cantidad_predicha,
            cantidad_descartada=venta.cantidad_descartada,
            cantidad_excedente=venta.cantidad_excedente,
            cantidad_normal=venta.cantidad_normal,
            id_plato=venta.id_plato
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        return nuevo_registro.id_venta_plato

    def obtener_por_id(self, id_venta: int) -> VentaPlato:
        model = VentaPlatoModel.query.get(id_venta)
        if not model:
            return None

        return VentaPlato(
            id_venta_plato=model.id_venta_plato,
            fecha=model.fecha,
            cantidad_predicha=model.cantidad_predicha,
            id_plato=model.id_plato,
            cantidad_normal=model.cantidad_normal,
            cantidad_excedente=model.cantidad_excedente,
            cantidad_descartada=model.cantidad_descartada,
            promo_enviada=model.promo_enviada
        )

    def actualizar(self, venta: VentaPlato) -> bool:
        model = VentaPlatoModel.query.get(venta.id_venta_plato)
        if not model:
            return False

        model.cantidad_normal = venta.cantidad_normal
        model.cantidad_excedente = venta.cantidad_excedente
        model.cantidad_descartada = venta.cantidad_descartada

        db.session.commit()
        return True

    def set_promo_enviada(self, id_venta: int, valor: bool) -> bool:
        model = VentaPlatoModel.query.get(id_venta)
        if not model:
            return False
        model.promo_enviada = valor
        db.session.commit()
        return True