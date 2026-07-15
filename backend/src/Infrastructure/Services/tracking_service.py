from src.Application.Services.itracking_service import ITrackingService
from src.Application.Dtos.tracking_dto import TrackingResponseDTO
from src.Application.Dtos.closing_dto import ClosingResponseDTO

DESCUENTO_TIERS = [
    (5, 10),
    (10, 20),
    (float('inf'), 30)
]

class TrackingService(ITrackingService):
    def __init__(self, venta_repository, plato_repository, cliente_repository, email_service):
        self.venta_repository = venta_repository
        self.plato_repository = plato_repository
        self.cliente_repository = cliente_repository
        self.email_service = email_service

    def _calcular_descuento(self, cantidad_restante):
        for limite, porcentaje in DESCUENTO_TIERS:
            if cantidad_restante <= limite:
                return porcentaje
        return 30

    def _enviar_promocion(self, plato, cantidad_restante, descuento, precio_descuento):
        clientes = self.cliente_repository.obtener_por_restaurante(plato.id_restaurante)
        if not clientes:
            print(f"NOTIFICACIÓN: no hay clientes registrados para el restaurante {plato.id_restaurante}")
            return
        asunto = f"¡Oferta especial en {plato.nombre}!"
        for cliente in clientes:
            cuerpo = (f"Hola {cliente.nombre},\n\n"
                      f"Quedan {cantidad_restante} unidades de '{plato.nombre}' hoy.\n"
                      f"Precio con {descuento}% de descuento: ${precio_descuento}\n\n"
                      f"¡Te esperamos!")
            self.email_service.enviar(cliente.email, asunto, cuerpo)

    def _enviar_agotado(self, plato):
        clientes = self.cliente_repository.obtener_por_restaurante(plato.id_restaurante)
        if not clientes:
            return
        asunto = f"{plato.nombre} agotado por hoy"
        for cliente in clientes:
            cuerpo = (f"Hola {cliente.nombre},\n\n"
                      f"'{plato.nombre}' ya se agotó por hoy. ¡Gracias por tu interés, vuelve pronto!")
            self.email_service.enviar(cliente.email, asunto, cuerpo)

    def verificar_riesgo(self, request):
        resultados = []
        for item in request.items:
            venta = self.venta_repository.obtener_por_id(item.id_venta_plato)
            if not venta:
                continue

            if venta.cantidad_predicha == 0:
                resultados.append(TrackingResponseDTO(
                    item.id_venta_plato, "SIN_DATOS", 0, 0, 0.0, False,
                    "No hay predicción registrada, no se puede calcular riesgo"))
                continue

            cantidad_restante = venta.cantidad_predicha - item.cantidad_vendida_actual

            if cantidad_restante <= 0:
                resultados.append(TrackingResponseDTO(
                    item.id_venta_plato, "SIN_EXCEDENTE", 0, 0, 0.0, False,
                    "No sobró nada, no se necesita promoción"))
                continue

            plato = self.plato_repository.obtener_por_id(venta.id_plato)
            descuento = self._calcular_descuento(cantidad_restante)
            precio_descuento = round(float(plato.precio) * (1 - descuento / 100), 2)

            notificado = False
            if not venta.promo_enviada:
                self._enviar_promocion(plato, cantidad_restante, descuento, precio_descuento)
                self.venta_repository.set_promo_enviada(venta.id_venta_plato, True)
                notificado = True

            mensaje = f"Quedan {cantidad_restante} unidades de '{plato.nombre}'. Descuento: {descuento}%"
            resultados.append(TrackingResponseDTO(
                item.id_venta_plato, "RIESGO", cantidad_restante, descuento, precio_descuento, notificado, mensaje))

        return resultados

    def enviar_notificacion(self, request):
        venta = self.venta_repository.obtener_por_id(request.id_venta_plato)
        if not venta:
            return False
        plato = self.plato_repository.obtener_por_id(venta.id_plato)
        if not plato:
            return False
        self._enviar_promocion(plato, venta.cantidad_predicha - venta.cantidad_normal, 0, 0.0)
        return True

    def cerrar_jornada(self, request):
        resultados = []
        for item in request.items:
            venta = self.venta_repository.obtener_por_id(item.id_venta_plato)
            if not venta:
                resultados.append(ClosingResponseDTO(item.id_venta_plato, False))
                continue

            if venta.promo_enviada and item.cantidad_descartada == 0:
                plato = self.plato_repository.obtener_por_id(venta.id_plato)
                if plato:
                    self._enviar_agotado(plato)

            venta.cantidad_normal = item.cantidad_normal
            venta.cantidad_excedente = item.cantidad_excedente
            venta.cantidad_descartada = item.cantidad_descartada

            exito = self.venta_repository.actualizar(venta)
            self.venta_repository.set_promo_enviada(item.id_venta_plato, False)

            resultados.append(ClosingResponseDTO(item.id_venta_plato, exito))

        return resultados