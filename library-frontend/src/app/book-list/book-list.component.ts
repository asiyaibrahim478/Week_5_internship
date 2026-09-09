import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { BookService } from '../book.service';
import { Book } from '../book.model';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-book-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './book-list.component.html',
  styleUrl: './book-list.component.css'
})
export class BookListComponent implements OnInit {
  books: Book[] = [];
  isLoading: boolean = false;
  errorMessage: string | null = null;
  notificationMessage: string | null = null;

  constructor(
    private bookService: BookService,
    public authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.isLoading = true;
    this.errorMessage = null;

    this.bookService.getBooks().subscribe({
      next: (data) => {
        this.books = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load books from backend API:', err);
        this.errorMessage = 'Unable to connect to the Library API. Please make sure the backend server is running.';
        this.isLoading = false;
      }
    });
  }

  deleteBook(id: number): void {
    if (!this.authService.isLoggedIn()) {
      this.errorMessage = 'You must be logged in as an Administrator to delete books.';
      return;
    }

    if (!this.authService.isAdmin()) {
      this.errorMessage = 'Permission denied: Only users with the Admin role are permitted to delete books.';
      return;
    }

    if (confirm('Are you sure you want to delete this book?')) {
      this.isLoading = true;
      this.bookService.deleteBook(id).subscribe({
        next: () => {
          this.notificationMessage = 'Book deleted successfully.';
          this.loadBooks();
          setTimeout(() => { this.notificationMessage = null; }, 3500);
        },
        error: (err) => {
          console.error('Error deleting book:', err);
          if (err.status === 403) {
            this.errorMessage = '403 Forbidden: Only Admin accounts have permission to delete books.';
          } else if (err.status === 401) {
            this.errorMessage = '401 Unauthorized: Session expired or invalid token. Please log in again.';
          } else {
            this.errorMessage = 'Failed to delete book. Please check server logs.';
          }
          this.isLoading = false;
        }
      });
    }
  }
}
