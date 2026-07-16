import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Plato {
  id_plato: number;
  nombre: string;
  precio: number;
}

@Injectable({ providedIn: 'root' })
export class PlatoService {
  private apiUrl = 'http://localhost:5000/api/platos';

  constructor(private http: HttpClient) {}

  listarTodos(): Observable<Plato[]> {
    return this.http.get<Plato[]>(this.apiUrl);
  }
}