import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BookService } from '../book.service';
import { Book } from '../book.model';

@Component({
  selector: 'app-book-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './book-list.component.html',
  styleUrl: './book-list.component.css'
})
export class BookListComponent implements OnInit {
  books: Book[] = [];
  isLoading: boolean = false;
  errorMessage: string | null = null;

  constructor(private bookService: BookService) {}

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
    if (confirm('Are you sure you want to delete this book?')) {
      this.isLoading = true;
      this.bookService.deleteBook(id).subscribe({
        next: () => {
          this.loadBooks();
        },
        error: (err) => {
          console.error('Error deleting book:', err);
          this.errorMessage = 'Failed to delete book. Please check server logs.';
          this.isLoading = false;
        }
      });
    }
  }
}
