import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Auth, LoginResponse } from '../services/auth';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {

  constructor(private auth: Auth, private router: Router) {}

  username = '';
  password = '';
  obscurePass = true;
  errorMsg = '';

  onLogin() {
    this.auth.login({ username: this.username, password: this.password }).subscribe({
      next: (res: LoginResponse) => {
        localStorage.setItem('token', res.token);
        localStorage.setItem('username', res.username);
        localStorage.setItem('id_restaurante', res.id_restaurante.toString());
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.errorMsg = 'Usuario o contraseña incorrectos';
        console.error('Error de login:', err);
      }
    });
  }
}