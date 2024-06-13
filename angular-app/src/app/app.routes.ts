import { Routes } from '@angular/router';

import { AuthGuard } from './guards/auth.guard';
import { PruebaComponent } from './components/prueba/prueba.component';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';


export const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
    { path: 'prueba', component: PruebaComponent }
];
