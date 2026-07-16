import { Component, OnInit, ElementRef, HostListener, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PredictionService, PredictionResult } from '../services/prediction';
import { PlatoService, Plato } from '../services/plato';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements OnInit {
  username = '';
  loading = false;
  errorMsg = '';
  resultados: PredictionResult[] = [];

  platosDisponibles: Plato[] = [];
  platosSeleccionados: Plato[] = [];
  busquedaPlato = '';
  mostrarSugerencias = false;

  clima = 1;
  tienePromo = false;
  esFestivo = false;

  constructor(
    private predictionService: PredictionService,
    private platoService: PlatoService,
    private router: Router,
    private elementRef: ElementRef
  ) {
    this.username = localStorage.getItem('username') || '';
  }

  @ViewChild('platoSelector')
  platoSelector!: ElementRef<HTMLElement>;

  @HostListener('document:click', ['$event'])
  clickFuera(event: MouseEvent) {
    if (
      this.mostrarSugerencias &&
      !this.platoSelector.nativeElement.contains(event.target as Node)
    ) {
      this.mostrarSugerencias = false;
    }
  }

  ngOnInit() {
    this.platoService.listarTodos().subscribe({
      next: (res) => this.platosDisponibles = res,
      error: () => this.errorMsg = 'No se pudo cargar la lista de platos'
    });
  }

  get sugerencias(): Plato[] {
    const termino = this.busquedaPlato.toLowerCase();
    return this.platosDisponibles.filter(p =>
      p.nombre.toLowerCase().includes(termino) &&
      !this.platosSeleccionados.some(sel => sel.id_plato === p.id_plato)
    );
  }

  agregarPlato(plato: Plato) {
    this.platosSeleccionados.push(plato);
    this.busquedaPlato = '';
    this.mostrarSugerencias = true;
  }

  quitarPlato(plato: Plato) {
    this.platosSeleccionados = this.platosSeleccionados.filter(
      p => p.id_plato !== plato.id_plato
    );
  }

  generar() {
    this.errorMsg = '';

    if (this.platosSeleccionados.length === 0) {
      this.errorMsg = 'Selecciona al menos un plato';
      return;
    }

    this.loading = true;
    this.predictionService.generarPrediccion({
      id_platos: this.platosSeleccionados.map(p => p.id_plato),
      clima: this.clima,
      es_festivo: this.esFestivo
    }).subscribe({
      next: (res) => {
        this.resultados = res;
        this.predictionService.guardarUltimaPrediccion(res);
        this.loading = false;
      },
      error: () => {
        this.errorMsg = 'No se pudo generar la predicción';
        this.loading = false;
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