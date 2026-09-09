import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  isRegisterMode = false;
  username = '';
  password = '';
  role = 'User';
  errorMessage = '';
  successMessage = '';
  isLoading = false;

  constructor(private authService: AuthService, private router: Router) {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/books']);
    }
  }

  toggleMode(): void {
    this.isRegisterMode = !this.isRegisterMode;
    this.errorMessage = '';
    this.successMessage = '';
  }

  onSubmit(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.username.trim() || !this.password.trim()) {
      this.errorMessage = 'Please enter both username and password.';
      return;
    }

    this.isLoading = true;

    if (this.isRegisterMode) {
      this.authService.register({
        username: this.username.trim(),
        password: this.password.trim(),
        role: this.role
      }).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.successMessage = 'Registration successful! You can now log in.';
          this.isRegisterMode = false;
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = err.error?.message || 'Registration failed. Please try again.';
        }
      });
    } else {
      this.authService.login({
        username: this.username.trim(),
        password: this.password.trim()
      }).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.router.navigate(['/books']);
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = err.error?.message || 'Invalid username or password.';
        }
      });
    }
  }
}
