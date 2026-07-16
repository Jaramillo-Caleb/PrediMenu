import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TrackingService, TrackingResult, FilaCierre } from '../services/tracking';
import { PredictionService, PredictionResult } from '../services/prediction';

interface FilaMonitoreo extends PredictionResult {
  cantidad_vendida_actual: number | null;
}

@Component({
  selector: 'app-monitoreo',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './monitoreo.html',
  styleUrl: './monitoreo.css'
})
export class Monitoreo implements OnInit {
  username = '';
  filas: FilaMonitoreo[] = [];

  resultadosRiesgo: TrackingResult[] = [];

  loadingRiesgo = false;
  errorMsg = '';

  constructor(
    private trackingService: TrackingService,
    private predictionService: PredictionService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {
    this.username = localStorage.getItem('username') || '';
  }

  ngOnInit() {
    const prediccion = this.predictionService.obtenerUltimaPrediccion();
    this.filas = prediccion.map(p => ({
      ...p,
      cantidad_vendida_actual: null
    }));
  }

  get hayRiesgo(): boolean {
    return this.resultadosRiesgo.some(r => r.estado === 'RIESGO');
  }

  verificarRiesgo() {
    this.errorMsg = '';

    if (this.filas.length === 0) {
      this.errorMsg = 'No hay predicción generada. Ve al Dashboard primero.';
      return;
    }

    const items = this.filas.map(f => ({
      id_venta_plato: f.id_venta_plato,
      cantidad_vendida_actual: f.cantidad_vendida_actual || 0
    }));

    this.loadingRiesgo = true;
    this.trackingService.verificarRiesgo(items).subscribe({
      next: (res) => {
        this.resultadosRiesgo = res;
        this.loadingRiesgo = false;

        if (this.hayRiesgo) {
          // Hay riesgo: pasamos las filas a Cierre para que el usuario las edite ahí
          const filasPendientes: FilaCierre[] = this.filas.map(f => ({
            id_venta_plato: f.id_venta_plato,
            nombre_plato: f.nombre_plato,
            cantidad_predicha: f.cantidad_predicha,
            cantidad_normal: f.cantidad_vendida_actual || 0,
            cantidad_excedente: 0
          }));
          this.trackingService.guardarFilasPendientesCierre(filasPendientes);
          this.router.navigate(['/cierre']);
        } else {
          this.cerrarAutomatico();
        }
      },
      error: () => {
        this.errorMsg = 'No se pudo verificar el riesgo';
        this.loadingRiesgo = false;
      }
    });
  }

  private cerrarAutomatico() {
    const items = this.filas.map(f => ({
      id_venta_plato: f.id_venta_plato,
      cantidad_normal: f.cantidad_vendida_actual || 0,
      cantidad_excedente: 0,
      cantidad_descartada: 0
    }));

    this.trackingService.cerrarJornada(items).subscribe({
      next: (res) => {
        this.trackingService.guardarUltimoCierre(res);
        this.predictionService.limpiarUltimaPrediccion();
        this.router.navigate(['/cierre']);
      },
      error: () => {
        this.errorMsg = 'No se pudo cerrar la jornada';
        this.cdr.detectChanges();
      }
    });
  }

  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }

  irA(ruta: string) {
    this.router.navigate([ruta]);
  }
}