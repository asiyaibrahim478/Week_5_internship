# Week 4 — Part B: Angular Authentication Integration

**Author:** Asiya  
**Project:** Library Management Frontend (Angular Standalone Components)

## Overview
Part B integrates the Angular Single Page Application (SPA) with the .NET Core JWT backend.

### Key Architectural Concepts
1. **`AuthService`:**
   - Centralized service holding authentication state, login/logout logic, token storage in `localStorage`, and token payload decoding (extracting user role and username).
2. **Functional HTTP Interceptor (`authInterceptor`):**
   - Implements `HttpInterceptorFn` registered in `app.config.ts` via `provideHttpClient(withInterceptors([authInterceptor]))`.
   - Clones outgoing HTTP requests and automatically injects `Authorization: Bearer <token>` when a token is present.
3. **Route Guards (`authGuard`):**
   - Implements `CanActivateFn` to guard protected navigation routes.
   - Redirects unauthorized visitors directly to `/login`.
4. **Role-Based UI Rendering:**
   - Evaluates whether the active user has the `Admin` role to display or hide sensitive operations like "Delete Book" and "Add Book".

---

## Token Storage Security Trade-offs
- **`localStorage`:** Easy to manage in SPAs and survives browser refreshes. Accessible by JavaScript (vulnerable to XSS if malicious scripts are injected).
- **`httpOnly` Cookies:** Immune to JavaScript/XSS reading, but requires CSRF protection and cross-origin cookie configuration.
- For this internship stage, `localStorage` is used alongside JWT Bearer headers.
