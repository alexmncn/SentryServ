import { Routes } from '@angular/router';

import { PruebaComponent } from './components/prueba/prueba.component';
import { HomeComponent } from './components/home/home.component';


export const routes: Routes = [
    { path: 'home', component: HomeComponent},
    { path: 'prueba', component: PruebaComponent }
];
