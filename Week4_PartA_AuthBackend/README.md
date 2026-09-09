# Week 4 — Part A: JWT Authentication in ASP.NET Core

**Author:** Asiya  
**Project:** Library Management API (ASP.NET Core Web API)

## Overview
Part A implements robust, production-standard JSON Web Token (JWT) authentication and role-based access control (RBAC).

### Key Architectural Concepts
1. **Password Hashing:**
   - Passwords are never stored in plaintext.
   - Utilizes ASP.NET Core's `PasswordHasher<User>` implementing PBKDF2 with HMAC-SHA256 and unique per-user cryptographic salts.
2. **Login & Token Issuance:**
   - The user submits credentials (`POST /api/auth/login`).
   - The server verifies `PasswordVerificationResult.Success`.
   - Generates a cryptographically signed HMAC-SHA256 JWT containing `ClaimTypes.NameIdentifier`, `ClaimTypes.Name`, and `ClaimTypes.Role`.
3. **Token Validation Middleware:**
   - Configured in `Program.cs` via `Microsoft.AspNetCore.Authentication.JwtBearer`.
   - Validates the token signature and expiration timestamp before requests reach protected controller actions.
4. **Endpoint Protection:**
   - `[Authorize]` protects data-modifying endpoints (`POST /api/books`, `PUT /api/books/{id}`).
   - `[Authorize(Roles = "Admin")]` restricts `DELETE /api/books/{id}` to Admin users only.
   - `GET /api/books` remains public for read access.

---

## API Endpoints Summary
| Method | Route | Auth Required | Permitted Roles | Description |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | No | Public | Register a new user with hashed password |
| `POST` | `/api/auth/login` | No | Public | Authenticate credentials and receive JWT |
| `GET` | `/api/books` | No | Public | Retrieve all books |
| `GET` | `/api/books/{id}` | No | Public | Retrieve single book |
| `POST` | `/api/books` | Yes (`Bearer JWT`) | All Authenticated Users | Add a new book |
| `PUT` | `/api/books/{id}` | Yes (`Bearer JWT`) | All Authenticated Users | Update an existing book |
| `DELETE`| `/api/books/{id}` | Yes (`Bearer JWT`) | `Admin` Only | Delete a book |
