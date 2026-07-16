import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router'; // 1. Importamos RouterOutlet

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class AppComponent {
  title = 'frontend';
}