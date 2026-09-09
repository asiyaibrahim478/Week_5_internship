import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface UserInfo {
  username: string;
  role: string;
}

export interface AuthResponse {
  token: string;
  username: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5252/api/auth';
  private tokenKey = 'library_jwt_token';
  private userKey = 'library_user_info';

  public currentUser = signal<UserInfo | null>(this.getStoredUser());
  public isLoggedInSignal = signal<boolean>(!!this.getToken());

  constructor(private http: HttpClient) {}

  login(credentials: { username: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, credentials).pipe(
      tap(res => {
        this.saveSession(res.token, { username: res.username, role: res.role });
      })
    );
  }

  register(data: { username: string; password: string; role?: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, data);
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.currentUser.set(null);
    this.isLoggedInSignal.set(false);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getUserRole(): string {
    const user = this.currentUser();
    return user ? user.role : '';
  }

  isAdmin(): boolean {
    return this.getUserRole().toLowerCase() === 'admin';
  }

  private saveSession(token: string, user: UserInfo): void {
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.userKey, JSON.stringify(user));
    this.currentUser.set(user);
    this.isLoggedInSignal.set(true);
  }

  private getStoredUser(): UserInfo | null {
    const data = localStorage.getItem(this.userKey);
    if (!data) return null;
    try {
      return JSON.parse(data);
    } catch {
      return null;
    }
  }
}
