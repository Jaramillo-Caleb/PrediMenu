import { Component, OnInit, ChangeDetectorRef  } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TrackingService, ClosingResult, FilaCierre } from '../services/tracking';
import { PredictionService } from '../services/prediction';

@Component({
  selector: 'app-cierre',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './cierre.html',
  styleUrl: './cierre.css',
})
export class Cierre implements OnInit {
  username = '';
  filasPendientes: FilaCierre[] = [];
  resultadosCierre: ClosingResult[] = [];
  loadingCierre = false;
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
    this.resultadosCierre = this.trackingService.obtenerUltimoCierre();
    this.filasPendientes = this.trackingService.obtenerFilasPendientesCierre();
  }

  get exitosos(): number {
    return this.resultadosCierre.filter(r => r.exito).length;
  }

  calcularDescartado(fila: FilaCierre): number {
    const normal = fila.cantidad_normal || 0;
    const excedente = fila.cantidad_excedente || 0;
    return Math.max(0, fila.cantidad_predicha - normal - excedente);
  }

  cerrarJornada() {
    this.errorMsg = '';

    const items = this.filasPendientes.map(f => ({
      id_venta_plato: f.id_venta_plato,
      cantidad_normal: f.cantidad_normal || 0,
      cantidad_excedente: f.cantidad_excedente || 0,
      cantidad_descartada: this.calcularDescartado(f)
    }));

    this.loadingCierre = true;
    this.trackingService.cerrarJornada(items).subscribe({
      next: (res) => {
        this.resultadosCierre = res;
        this.loadingCierre = false;
        this.trackingService.guardarUltimoCierre(res);
        this.trackingService.limpiarFilasPendientesCierre();
        this.predictionService.limpiarUltimaPrediccion();
        this.filasPendientes = [];
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMsg = 'No se pudo cerrar la jornada';
        this.loadingCierre = false;
      }
    });
  }

  nuevaJornada() {
    this.trackingService.limpiarUltimoCierre();
    this.router.navigate(['/dashboard']);
  }

  logout() {
    localStorage.clear();
    this.trackingService.limpiarUltimoCierre();
    this.trackingService.limpiarFilasPendientesCierre();
    this.predictionService.limpiarUltimaPrediccion();
    this.router.navigate(['/login']);
  }

  irA(ruta: string) {
    this.router.navigate([ruta]);
  }
}