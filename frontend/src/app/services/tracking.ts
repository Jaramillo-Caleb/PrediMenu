import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface TrackingItemRequest {
  id_venta_plato: number;
  cantidad_vendida_actual: number;
}

export interface TrackingResult {
  id_venta_plato: number;
  estado: string;
  cantidad_restante: number;
  descuento: number;
  precio_descuento: number;
  notificado: boolean;
  mensaje: string;
}

export interface ClosingItemRequest {
  id_venta_plato: number;
  cantidad_normal: number;
  cantidad_excedente: number;
  cantidad_descartada: number;
}

export interface ClosingResult {
  id_venta_plato: number;
  exito: boolean;
}

// Fila editable que Monitoreo pasa a Cierre cuando hay riesgo
export interface FilaCierre {
  id_venta_plato: number;
  nombre_plato: string;
  cantidad_predicha: number;
  cantidad_normal: number;
  cantidad_excedente: number;
}

interface TrackingResultBackend {
  id_venta_plato: number;
  status: string;
  cantidad_restante: number;
  descuento_pct: number;
  precio_descuento: number;
  notificado: boolean;
  mensaje: string;
}

interface ClosingResultBackend {
  id_venta_plato: number;
  actualizado: boolean;
}

@Injectable({ providedIn: 'root' })
export class TrackingService {
  private apiUrl = 'http://localhost:5000/api';

  // Estado compartido: sobrevive la navegación entre Monitoreo y Cierre
  private filasPendientesCierre: FilaCierre[] = [];
  private ultimoCierre: ClosingResult[] = [];

  constructor(private http: HttpClient) {}

  verificarRiesgo(items: TrackingItemRequest[]): Observable<TrackingResult[]> {
    return this.http.post<TrackingResultBackend[]>(`${this.apiUrl}/seguimiento/verificar`, { items })
      .pipe(map(res => res.map(r => ({
        id_venta_plato: r.id_venta_plato,
        estado: r.status,
        cantidad_restante: r.cantidad_restante,
        descuento: r.descuento_pct,
        precio_descuento: r.precio_descuento,
        notificado: r.notificado,
        mensaje: r.mensaje
      }))));
  }

  cerrarJornada(items: ClosingItemRequest[]): Observable<ClosingResult[]> {
    return this.http.put<ClosingResultBackend[]>(`${this.apiUrl}/ventas/cierre`, { items })
      .pipe(map(res => res.map(r => ({
        id_venta_plato: r.id_venta_plato,
        exito: r.actualizado
      }))));
  }

  // --- Filas pendientes de cierre (caso con riesgo, requiere edición) ---
  guardarFilasPendientesCierre(filas: FilaCierre[]) {
    this.filasPendientesCierre = filas;
  }

  obtenerFilasPendientesCierre(): FilaCierre[] {
    return this.filasPendientesCierre;
  }

  limpiarFilasPendientesCierre() {
    this.filasPendientesCierre = [];
  }

  // --- Resultado final de cierre ---
  guardarUltimoCierre(resultados: ClosingResult[]) {
    this.ultimoCierre = resultados;
  }

  obtenerUltimoCierre(): ClosingResult[] {
    return this.ultimoCierre;
  }

  limpiarUltimoCierre() {
    this.ultimoCierre = [];
  }
}