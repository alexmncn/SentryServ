// dispositivo.service.ts
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PruebaService {
  private apiUrl = 'http://172.0.0.1:8000/mqtt-service/status';

  constructor(private http: HttpClient) { }

  obtenerEstado(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
    //return of({ "pc-status": { "status-data": "Connected" } });

  }
}

