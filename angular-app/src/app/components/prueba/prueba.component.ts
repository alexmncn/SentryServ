import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PruebaService } from '../../services/prueba/prueba.service'; 

@Component({
  selector: 'app-prueba',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './prueba.component.html',
  styleUrl: './prueba.component.css'
})
export class PruebaComponent implements OnInit{
  public sensor_name: string ="";
  public temperature: number =0.0;
  public humidity: number =0.0;
  public battery: number =0.0;

  constructor(private pruebaService: PruebaService) { }

  ngOnInit(): void {
    this.obtenerEstadoDispositivo();
  }

  obtenerEstadoDispositivo(): void {
    this.pruebaService.obtenerEstado()
      .subscribe(data => {
        this.sensor_name = data['sensor_name']['status-data']
        this.temperature = data['temperature']['status-data'];
        this.humidity = data['humidity']['status-data'];
        this.battery = data['battery']['status-data'];
      });
  }
}
