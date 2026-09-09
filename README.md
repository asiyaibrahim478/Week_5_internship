# 📚 Library Management System & AI Service (Week 4 Milestone)

**Author / Intern:** Asiya  
**Repository:** [`asiyaibrahim478/week4_internship`](https://github.com/asiyaibrahim478/week4_internship.git)  
**Milestone Version:** `v0.4-week4`

[![Repository: week4_internship](https://img.shields.io/badge/Repo-asiyaibrahim478%2Fweek4__internship-blue)](https://github.com/asiyaibrahim478/week4_internship)
[![Framework: .NET 8](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![Frontend: Angular](https://img.shields.io/badge/Frontend-Angular-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![AI Microservice: FastAPI](https://img.shields.io/badge/AI_Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Database: SQL Server & EF Core](https://img.shields.io/badge/Database-SQL_Server_%26_EF_Core-CC292B?logo=microsoftsqlserver&logoColor=white)](https://learn.microsoft.com/en-us/ef/core/)

---

## 🌟 Overview & Week 4 Objectives

Week 4 advances the system into an enterprise-grade secure architecture and expands the Python AI capabilities into a dedicated microservice:
1. **Part A (.NET Core JWT Auth & RBAC):** Production password hashing using `PasswordHasher<User>`, JWT generation with HMAC-SHA256 signing, validation middleware, and role-based endpoint authorization (`[Authorize]`, `[Authorize(Roles = "Admin")]`).
2. **Part B (Angular Authentication & Protection):** Centralized `AuthService`, functional HTTP `authInterceptor` injecting Bearer headers, `authGuard` route protection, and dynamic role-based UI visibility.
3. **Part C, D, E (FastAPI AI Backend & Prompt Engineering):** Asynchronous FastAPI microservice (`ai-service`), Pydantic validation, structured JSON outputs, streaming simulations, conversation history, few-shot conditioning, and prompt injection defenses.
4. **Part F (Git Collaboration Level Up):** Branch protection, standardized Pull Request templates (`.github/PULL_REQUEST_TEMPLATE.md`), and merge conflict resolution.

---

## 🔄 Architecture & Data Flow

```mermaid
flowchart TD
    subgraph Client["Frontend SPA (Angular)"]
        UI["UI / Book List / Login View"]
        AuthSvc["AuthService (localStorage JWT)"]
        Interceptor["Functional authInterceptor"]
    end

    subgraph BackendAPI[".NET 8 Web API (:5252)"]
        JwtMiddleware["JWT Validation Middleware"]
        AuthCtrl["AuthController (/api/auth)"]
        BooksCtrl["BooksController (/api/books)"]
        EF["Entity Framework Core"]
        DB[(SQL Server / InMemory)]
    end

    subgraph AIService["Python FastAPI AI Service (:8000)"]
        FastAPIServer["FastAPI Application"]
        PydanticModels["Pydantic Validation"]
        PromptEngine["Engineered Prompt Templates"]
    end

    UI -->|1. Submit Login| AuthCtrl
    AuthCtrl -->|2. Verify Hash & Issue JWT| AuthSvc
    UI -->|3. API Request with Bearer Token| Interceptor
    Interceptor -->|4. Authenticated Request| JwtMiddleware
    JwtMiddleware -->|5. Check Claims & Roles| BooksCtrl
    BooksCtrl --> EF --> DB

    UI -.->|Independent AI Invocations| FastAPIServer
    FastAPIServer --> PydanticModels --> PromptEngine
```

> [!NOTE]
> The .NET Web API and Python FastAPI AI microservice remain independent services in Week 4. Direct backend-to-backend orchestration will be integrated in Week 6.

---

## 🏗️ Repository Structure

```text
├── LibraryAPI/                       # ASP.NET Core 8 Web API
│   ├── Controllers/                  # AuthController (JWT, Register, Login), BooksController
│   ├── Data/                         # LibraryDbContext (EF Core)
│   ├── DTOs/                         # RegisterDto, LoginDto, AuthResponseDto
│   ├── Models/                       # Book, Author, Category, User
│   ├── Repositories/                 # IBookRepository, BookRepository, InMemoryBookRepository
│   ├── Services/                     # IBookService, BookService
│   ├── appsettings.Development.json  # JWT Secrets (Development)
│   └── Program.cs                    # JWT Auth Scheme, Swagger Bearer, CORS, Pipeline
│
├── library-frontend/                 # Angular 17/18 Standalone Client
│   ├── src/app/
│   │   ├── components/login/         # Reactive Login & Register component
│   │   ├── book-list/                # Book catalog with Admin-conditional actions
│   │   ├── book-form/                # Guarded Book creation form
│   │   ├── services/                 # AuthService (JWT state, signals)
│   │   ├── interceptors/             # Functional authInterceptor
│   │   ├── guards/                   # Functional authGuard
│   │   ├── app.config.ts             # withInterceptors([authInterceptor])
│   │   └── app.routes.ts             # Route configurations with authGuard
│
├── ai-service/                       # FastAPI AI Microservice (Python)
│   ├── main.py                       # FastAPI application & Pydantic endpoints
│   ├── prompts.py                    # Zero-Shot, Few-Shot & Role-based Prompt Templates
│   ├── requirements.txt              # FastAPI, Uvicorn, Pydantic dependencies
│   └── README.md                     # Microservice guide & test curl commands
│
├── Week4_PartA_AuthBackend/          # Part A documentation & test commands
├── Week4_PartB_AngularAuth/          # Part B architecture notes & interceptor design
├── Week4_PartC_FastAPI/              # Part C FastAPI foundations & OpenAPI notes
├── Week4_PartD_LLM/                  # Part D LLM scripts (History, Streaming, JSON)
├── Week4_PartE_PromptEngineering/    # Part E Prompt experiments & injection tests
├── Week4_PartF_GitPractice/          # Part F Merge conflict resolution guide
├── Week4_CheckStage_Answers.md       # Comprehensive check stage questions & answers
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md      # Standardized PR template
└── README.md                         # Project documentation
```

---

## 🚀 How to Run the Applications

### 1. Backend (.NET 8 Web API)
```bash
cd LibraryAPI
dotnet build
dotnet run
```
- **API URL:** `http://localhost:5252`
- **Swagger Documentation:** `http://localhost:5252/swagger` (Use the **Authorize** lock button to supply your Bearer JWT).

### 2. Frontend (Angular Client)
```bash
cd library-frontend
npm install
npm start
```
- **Web UI:** `http://localhost:4200`
- **Demo Accounts:**
  - **Admin User:** `admin` / `Admin123!` (Full permissions + Delete)
  - **Standard User:** `Asiya` / `password123` (View / Add / Edit)

### 3. AI Microservice (FastAPI + Python)
```bash
cd ai-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`

---

## 📡 REST API Specifications

### Authentication Endpoints (`LibraryAPI`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Public | Registers a new user with hashed password |
| `POST` | `/api/auth/login` | Public | Validates credentials and returns JWT Bearer token |

### Book Catalog Endpoints (`LibraryAPI`)
| Method | Endpoint | Required Authorization | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/books` | Public | Retrieves all books |
| `GET` | `/api/books/{id}` | Public | Retrieves a single book by ID |
| `POST` | `/api/books` | `Bearer JWT` (Any User) | Adds a new book |
| `PUT` | `/api/books/{id}` | `Bearer JWT` (Any User) | Updates an existing book |
| `DELETE` | `/api/books/{id}` | `Bearer JWT` (`Admin` role only) | Removes a book (403 for non-admins) |

### AI Microservice Endpoints (`ai-service`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health probe & service metadata |
| `POST` | `/summarize` | Returns structured JSON summary & genre classification |
| `POST` | `/genre-suggestion` | Few-shot conditioned genre categorization |
| `POST` | `/prompt-injection-test` | Demonstrates defensive input isolation |

---

## 🛡️ Git Workflow & Conventional Commits

Commit history adheres to conventional commit formatting:
- `feat:` Feature implementations (`feature/jwt-auth-backend`, `feature/angular-auth`, `feature/ai-fastapi-service`)
- `fix:` Bug fixes and conflict resolutions
- `docs:` Documentation updates
- `chore:` Configuration and PR templates

**Milestone Release Tag:** `v0.4-week4`
