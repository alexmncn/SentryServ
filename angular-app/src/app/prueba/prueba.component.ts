import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PruebaService } from '../prueba.service';

@Component({
  selector: 'app-prueba',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './prueba.component.html',
  styleUrl: './prueba.component.css'
})
export class PruebaComponent implements OnInit{
  estado: string= '';

  constructor(private pruebaService: PruebaService) { }

  ngOnInit(): void {
    this.obtenerEstadoDispositivo();
  }

  obtenerEstadoDispositivo(): void {
    this.pruebaService.obtenerEstado()
      .subscribe(data => {
        this.estado = data['pc-status']['status-data'];
        console.log(this.estado);
      });
  }
}
