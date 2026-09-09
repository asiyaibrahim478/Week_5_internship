# 📚 internship-project-week-3 (Week 3 Milestone)

[![Repository: internship-project-week-3](https://img.shields.io/badge/Repo-internship--project--week--3-blue)](https://github.com/)
[![Framework: .NET 8](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![Frontend: Angular](https://img.shields.io/badge/Frontend-Angular-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![Database: SQL Server & EF Core](https://img.shields.io/badge/Database-SQL_Server_%26_EF_Core-CC292B?logo=microsoftsqlserver&logoColor=white)](https://learn.microsoft.com/en-us/ef/core/)
[![AI Track: Python](https://img.shields.io/badge/AI_Track-Python_3-3776AB?logo=python&logoColor=white)](https://python.org/)

---

## 🌟 Overview & Architecture

This repository (**`internship-project-week-3`**) contains the full source code and database architecture for the **Library Management System** created during the 8-Week AI Software Development Internship. 

In **Week 3**, the system transitioned from in-memory collections to a persistent **SQL Server database managed with Entity Framework Core (Code-First & Migrations)**, fully integrated with a **live Angular client using HttpClient** and standalone **AI foundation scripts**.

### 🔄 End-to-End Data Flow
```mermaid
flowchart LR
    User([User Browser]) -->|UI Interaction| Angular[Angular Frontend / HttpClient]
    Angular -->|HTTP REST JSON| Controller[ASP.NET Core Controller]
    Controller -->|Calls| Service[Service Layer (IBookService)]
    Service -->|Calls| Repository[Repository Layer (IBookRepository)]
    Repository -->|LINQ Queries| EFCore[Entity Framework Core DbContext]
    EFCore -->|T-SQL Queries| SQLServer[(SQL Server Database)]
```

---

## 🏗️ Repository Structure

```text
├── LibraryAPI/                    # ASP.NET Core 8 Web API backend
│   ├── Controllers/               # BooksController, AuthController
│   ├── Data/                      # LibraryDbContext (EF Core)
│   ├── Models/                    # Book, Author, Category, User entities
│   ├── Repositories/              # IBookRepository, EF Core BookRepository
│   ├── Services/                  # IBookService, BookService
│   ├── appsettings.json           # Database connection strings
│   └── Program.cs                 # DI container, CORS, DbContext config
│
├── library-frontend/              # Angular 17/18 Standalone client
│   ├── src/app/
│   │   ├── book-list/             # Book catalog with loading & error states
│   │   ├── book-form/             # Reactive form for adding new books
│   │   ├── book.service.ts        # HttpClient service interacting with API
│   │   └── book.model.ts          # TypeScript interfaces
│   └── src/environments/         # Environment API endpoints
│
├── Week3_PartA_SQL/               # Relational SQL Scripts
│   ├── 01_create_tables.sql       # Schema with PK, FK, many-to-many tables
│   ├── 02_insert_sample_data.sql  # Sample authors, books, categories
│   └── 03_join_queries.sql        # INNER JOIN, Many-to-Many & FK integrity tests
│
├── Week3_PartD_Auth/              # Authentication Foundations
│   └── week3-auth-notes.md        # AuthN vs AuthZ, Password Hashing, JWT anatomy
│
├── Week3_PartG_AIScripts/         # AI Foundations Track
│   ├── main.py                    # Standalone Python LLM script (Claude/Gemini/OpenAI)
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Template for API keys
│
├── .gitignore                     # Git ignore rules for .NET, Angular, Python
└── README.md                      # Project documentation
```

---

## 🚀 How to Run the Applications

### 1. Backend (.NET 8 Web API)
```bash
cd LibraryAPI

# Restore & Build
dotnet build

# Run the API server (Default URL: http://localhost:5252)
dotnet run
```
> **Swagger UI**: Navigate to `http://localhost:5252/swagger` to inspect and test all endpoints interactively.

---

### 2. Frontend (Angular Client)
```bash
cd library-frontend

# Install dependencies (first time only)
npm install

# Start Angular Development Server
npm start
# or
ng serve --open
```
> Navigate to `http://localhost:4200` to interact with the live Library UI.

---

### 3. AI Foundations Script (Python)
```bash
cd Week3_PartG_AIScripts

# 1. Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
copy .env.example .env
# Edit .env and paste your ANTHROPIC_API_KEY or OPENAI_API_KEY / GEMINI_API_KEY

# 4. Run the AI script
python main.py
```

---

## 📡 REST API Endpoints

| Method | Endpoint | Description | Request Body | Response Status |
|---|---|---|---|---|
| `GET` | `/api/books` | Retrieves all books with authors & categories | None | `200 OK` |
| `GET` | `/api/books/{id}` | Retrieves a single book by ID | None | `200 OK` / `404 Not Found` |
| `POST` | `/api/books` | Creates a new book entry in the database | `Book` JSON | `201 Created` |
| `PUT` | `/api/books/{id}` | Updates an existing book | `Book` JSON | `204 No Content` / `400` / `404` |
| `DELETE` | `/api/books/{id}` | Deletes a book from the library | None | `204 No Content` / `404 Not Found` |
| `POST` | `/api/auth/login` | Login foundation endpoint (Skeleton for Week 4) | `{ "username", "password" }` | `200 OK` / `401 Unauthorized` |

---

## 🛡️ Git Workflow & Commit Conventions

Commit messages strictly adhere to the [Conventional Commits](https://www.conventionalcommits.org/) standard:
- `feat:` New features or capabilities
- `fix:` Bug fixes
- `docs:` Documentation or concept notes
- `chore:` Configuration, dependencies, migrations
- `refactor:` Code restructuring without behavior changes

### Milestone Tag
- **Version Tag**: `v0.3-week3`
