// prueba.service.ts
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PruebaService {
  private apiUrl = 'http://127.0.0.1:8000/sensors/last-sensor-entry/1';

  constructor(private http: HttpClient) { }

  obtenerEstado(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
    /*return of({
      "battery": {
        "status-data": "87.9 %"
      },
      "date": {
        "status-data": "Tue, 11 Jun 2024 16:55:59 GMT"
      },
      "humidity": {
        "status-data": "45.8 %"
      },
      "sensor_name": {
        "status-data": "sensor1"
      },
      "temperature": {
        "status-data": "25.5 \u00baC"
      }
    }
    );
    */
  }
}

