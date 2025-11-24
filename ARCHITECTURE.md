# Django Todo App - System Architecture

This document provides visual diagrams to help understand how the Django Todo application works.

---

## Application Architecture

### High-Level Overview

```mermaid
graph TB
    User[👤 User Browser] -->|HTTP Request| Nginx[Nginx Web Server]
    Nginx -->|Proxy Pass| Gunicorn[Gunicorn WSGI Server]
    Gunicorn -->|WSGI| Django[Django Application]
    Django -->|ORM Queries| DB[(SQLite/PostgreSQL Database)]
    Django -->|Read| Static[Static Files CSS/JS]
    Django -->|Render| Templates[HTML Templates]
    Templates -->|Response| Gunicorn
    Gunicorn -->|HTTP Response| Nginx
    Nginx -->|HTML/CSS/JS| User
```

**ELI5**: When you visit the website, your browser talks to Nginx (the doorman), who passes your request to Gunicorn (the messenger), who gives it to Django (the brain). Django gets data from the database, creates an HTML page, and sends it back through the same chain.

---

## Django MVT Architecture

```mermaid
graph LR
    Browser[🌐 Browser] -->|1. Request URL| URLs[URLs Router]
    URLs -->|2. Route to View| View[View Logic]
    View -->|3. Query Data| Model[Model ORM]
    Model -->|4. Database Query| DB[(Database)]
    DB -->|5. Return Data| Model
    Model -->|6. Data Objects| View
    View -->|7. Context Data| Template[Template Engine]
    Template -->|8. Render HTML| View
    View -->|9. HTTP Response| Browser
    
    style Model fill:#e1f5ff
    style View fill:#fff4e1
    style Template fill:#f0ffe1
```

**Explanation**:
1. **Browser** requests `/todos/`
2. **URLs** matches pattern and routes to `TodoListView`
3. **View** asks Model for all todos
4. **Model** queries the database
5. **Database** returns todo records
6. **Model** converts to Python objects
7. **View** passes data to template
8. **Template** renders HTML with the data
9. **View** sends HTML back to browser

---

## Request-Response Cycle

```mermaid
sequenceDiagram
    participant U as User
    participant N as Nginx
    participant G as Gunicorn
    participant D as Django
    participant DB as Database
    
    U->>N: GET /todos/
    N->>G: Forward request
    G->>D: WSGI call
    D->>D: URL routing
    D->>D: View processing
    D->>DB: SELECT * FROM todos
    DB-->>D: Todo records
    D->>D: Render template
    D-->>G: HTML response
    G-->>N: HTTP response
    N-->>U: Display page
```

---

## Database Schema

```mermaid
erDiagram
    TODO {
        int id PK
        string title
        text description
        datetime due_date
        boolean is_resolved
        datetime created_at
        datetime updated_at
    }
```

**Fields Explained**:
- `id`: Unique identifier (auto-generated)
- `title`: The todo's name (required)
- `description`: Extra details (optional)
- `due_date`: When it's due (optional)
- `is_resolved`: Completed or not (default: false)
- `created_at`: When it was created (auto)
- `updated_at`: Last modification time (auto)

---

## CRUD Operations Flow

### Create Todo

```mermaid
graph TD
    A[User clicks 'Add Todo'] --> B[GET /create/]
    B --> C[TodoCreateView]
    C --> D[Display TodoForm]
    D --> E[User fills form]
    E --> F[POST /create/]
    F --> G[Validate form]
    G -->|Valid| H[Save to database]
    G -->|Invalid| D
    H --> I[Redirect to list]
    I --> J[Show success message]
```

### Read Todos

```mermaid
graph TD
    A[User visits /] --> B[TodoListView]
    B --> C[Query all todos]
    C --> D[Order by created_at DESC]
    D --> E[Pass to template]
    E --> F[Render home.html]
    F --> G[Display list with badges]
```

### Update Todo

```mermaid
graph TD
    A[User clicks Edit] --> B[GET /id/update/]
    B --> C[TodoUpdateView]
    C --> D[Load todo from DB]
    D --> E[Pre-fill form]
    E --> F[User modifies]
    F --> G[POST /id/update/]
    G --> H[Validate]
    H -->|Valid| I[Update database]
    H -->|Invalid| E
    I --> J[Redirect to list]
```

### Delete Todo

```mermaid
graph TD
    A[User clicks Delete] --> B[GET /id/delete/]
    B --> C[TodoDeleteView]
    C --> D[Show confirmation page]
    D --> E[User confirms]
    E --> F[POST /id/delete/]
    F --> G[Delete from database]
    G --> H[Redirect to list]
    H --> I[Show success message]
```

---

## Deployment Architecture

### Raspberry Pi Setup

```mermaid
graph TB
    Internet[🌐 Internet] -->|Port 80/443| Router[Home Router]
    Router -->|Port Forward| RPi[Raspberry Pi]
    
    subgraph "Raspberry Pi"
        Nginx[Nginx :80] -->|Proxy| Gunicorn[Gunicorn :8000]
        Gunicorn --> Django[Django App]
        Django --> SQLite[(SQLite DB)]
        Supervisor[Supervisor] -.Manages.-> Gunicorn
    end
    
    style RPi fill:#f9f,stroke:#333,stroke-width:2px
```

### Cloud Deployment (Railway/Render)

```mermaid
graph TB
    Internet[🌐 Internet] -->|HTTPS| CDN[CDN/Load Balancer]
    CDN --> App[Django Container]
    App --> DB[(PostgreSQL)]
    App --> Redis[(Redis Cache)]
    
    GitHub[GitHub Repo] -.Auto Deploy.-> App
    
    style App fill:#e1f5ff
    style DB fill:#ffe1e1
    style Redis fill:#fff4e1
```

---

## Form Validation Flow

```mermaid
graph TD
    A[User submits form] --> B{Is POST?}
    B -->|No| C[Show empty form]
    B -->|Yes| D[Create form with data]
    D --> E{Is valid?}
    E -->|No| F[Show errors]
    F --> C
    E -->|Yes| G{Custom validation}
    G -->|Fail| F
    G -->|Pass| H[Save to database]
    H --> I[Add success message]
    I --> J[Redirect to list]
```

**Custom Validation Example**:
- Check if due_date is not in the past
- Ensure title is not empty
- Validate field lengths

---

## Authentication Flow (Future Enhancement)

```mermaid
sequenceDiagram
    participant U as User
    participant L as Login View
    participant D as Django Auth
    participant DB as Database
    participant S as Session
    
    U->>L: Enter credentials
    L->>D: Authenticate
    D->>DB: Check user
    DB-->>D: User data
    D->>D: Verify password
    D->>S: Create session
    S-->>U: Set cookie
    U->>U: Access protected pages
```

---

## Static Files Serving

### Development

```mermaid
graph LR
    Browser[Browser] -->|Request /static/style.css| Django[Django Dev Server]
    Django -->|Serve directly| Static[Static Files]
    Static -->|CSS/JS| Browser
```

### Production

```mermaid
graph LR
    Browser[Browser] -->|Request /static/style.css| Nginx[Nginx]
    Nginx -->|Serve directly| Static[Static Files Directory]
    Static -->|CSS/JS| Browser
    
    Django[Django App] -.collectstatic.-> Static
```

**Why different?**
- **Development**: Django serves static files (slow but convenient)
- **Production**: Nginx serves static files (fast and efficient)

---

## Testing Pyramid

```mermaid
graph TD
    A[Unit Tests] -->|Test Models| B[Model Tests]
    A -->|Test Forms| C[Form Tests]
    D[Integration Tests] -->|Test Views| E[View Tests]
    D -->|Test URLs| F[URL Tests]
    G[E2E Tests] -->|Browser Tests| H[Selenium/Playwright]
    
    style A fill:#e1ffe1
    style D fill:#fff4e1
    style G fill:#ffe1e1
```

**Our Coverage**:
- ✅ Model Tests (creation, defaults, str)
- ✅ View Tests (GET/POST for all CRUD)
- ⚪ Form Tests (could add)
- ⚪ E2E Tests (could add)

---

## Performance Optimization Layers

```mermaid
graph TB
    Request[User Request] --> Cache{In Cache?}
    Cache -->|Yes| Return[Return Cached]
    Cache -->|No| DB[Query Database]
    DB --> Process[Process Data]
    Process --> Store[Store in Cache]
    Store --> Return
    
    style Cache fill:#fff4e1
    style DB fill:#ffe1e1
```

**Future Enhancements**:
1. Add Redis for caching
2. Database query optimization
3. CDN for static files
4. Lazy loading for images

---

## Security Layers

```mermaid
graph TD
    Request[HTTP Request] --> HTTPS{HTTPS?}
    HTTPS -->|No| Reject[Reject/Redirect]
    HTTPS -->|Yes| CSRF{Valid CSRF?}
    CSRF -->|No| Reject
    CSRF -->|Yes| Auth{Authenticated?}
    Auth -->|No| Login[Redirect to Login]
    Auth -->|Yes| Perm{Has Permission?}
    Perm -->|No| Forbidden[403 Forbidden]
    Perm -->|Yes| Process[Process Request]
    
    style HTTPS fill:#e1ffe1
    style CSRF fill:#fff4e1
    style Auth fill:#ffe1e1
```

**Current Security**:
- ✅ CSRF protection (Django default)
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection (template escaping)
- ⚪ HTTPS (needs configuration)
- ⚪ Authentication (not implemented yet)

---

## Monitoring & Logging

```mermaid
graph LR
    App[Django App] -->|Errors| Sentry[Sentry Error Tracking]
    App -->|Logs| Files[Log Files]
    App -->|Metrics| Monitor[Monitoring Dashboard]
    
    Files --> Analyze[Log Analysis]
    Monitor --> Alert[Alerts]
    
    style Sentry fill:#ffe1e1
    style Monitor fill:#e1f5ff
```

---

These diagrams provide a visual understanding of how the Django Todo application works at different levels. Use them as reference when learning or explaining the system to others!
