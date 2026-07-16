import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PredictionResult {
  id_venta_plato: number;
  id_plato: number;
  nombre_plato: string;
  cantidad_predicha: number;
}

export interface PredictionRequest {
  id_platos: number[];
  clima: number;
  es_festivo: boolean;
}

@Injectable({ providedIn: 'root' })
export class PredictionService {
  private apiUrl = 'http://localhost:5000/api/prediccion';
  private readonly storageKey = 'ultima_prediccion';

  constructor(private http: HttpClient) {}

  generarPrediccion(payload: PredictionRequest): Observable<PredictionResult[]> {
    return this.http.post<PredictionResult[]>(`${this.apiUrl}/generar`, payload);
  }

  guardarUltimaPrediccion(resultados: PredictionResult[]) {
    localStorage.setItem(this.storageKey, JSON.stringify(resultados));
  }

  obtenerUltimaPrediccion(): PredictionResult[] {
    const raw = localStorage.getItem(this.storageKey);
    return raw ? JSON.parse(raw) : [];
  }

  limpiarUltimaPrediccion() {
    localStorage.removeItem(this.storageKey);
  }
}