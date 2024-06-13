import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';
import { environment } from '../../enviroment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private logInUrl = environment.apiUrl + '/login';
  private logOutUrl = environment.apiUrl + '/logout';

  public username: string='';

  constructor(private http: HttpClient, private cookieService: CookieService) { }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(this.logInUrl, {username, password})
  }

  // Clear user data
  logout(): void {     
    this.clearToken();
    localStorage.clear();
  }

  // Request to backend logout
  logoutReq(): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': 'Bearer ' + this.getToken()
    });
    return this.http.post<any>(this.logOutUrl, {}, { headers })
  }

  // JWTtoken cookie
  storeToken(token: string): void {
    this.cookieService.set('authToken', token, 1, '/', undefined, true, 'Strict');
  }

  getToken(): string | null {
    return this.cookieService.get('authToken');
  }

  clearToken(): void {
    this.cookieService.delete('authToken');
  }


  // User
  setUsername(username: string): void {
    localStorage.setItem('username', username);
  }

  getUsername(): string | null {
    return localStorage.getItem('username');
  }
}
