import { Routes } from '@angular/router';
import { Login } from './login/login';
import { Dashboard } from './dashboard/dashboard';
import { Monitoreo } from './monitoreo/monitoreo';
import { Cierre } from './cierre/cierre';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'dashboard', component: Dashboard, canActivate: [authGuard] },
  { path: 'monitoreo', component: Monitoreo, canActivate: [authGuard] },
  { path: 'cierre', component: Cierre, canActivate: [authGuard] },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
];