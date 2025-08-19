# DocuChatAPI Project Architecture

## Overview

This document describes the architecture of the DocuChat API project.
The design follows modular principles, clean separation of concerns, and 3-tier 
architecture:

`Model ➝ Service ➝ Controller`

**Core Components:**

- **FastAPI API** – Exposes endpoints for authentication, session management, 
document upload, chat, and usage tracking.  

- **Database (PostgresSQL + SQLModel)** – Stores structured application data.

- **Vector Store (FAISS / Pinecone / Weaviate, pluggable)** – Manages embeddings for 
document search.  

- **Authentication & Middleware** – JWT or OAuth2 authentication for secure API access.

- **Business Logic Services** – Handle session lifecycle, token accounting, and limits. 

- **LLM Integration (OpenAI / Local LLMs)** – Provides intelligent responses enhanced 
by context retrieval.

## Project Structure

```commandline
src/
|── abstractions/           # Contains OOP abstractions/interfaces
│── api/
│   └── v1/
│       ├── controllers/    # Handle API logic, orchestrate services
│       ├── routes/         # Define API endpoints (FastAPI routers)
│       └── __init__.py
│
│── config/                 # Configuration files (settings, environment, logging)
│
│── data/                   # Contains app data
│
│── database/
│   ├── models/             # SQLModel classes (ORM representations of tables)
│   ├── schemas/            # Pydantic schemas for request/response validation
│   ├── db_connection.py    # Database connection & session management
│   └── __init__.py
│
│── middleware/             # Custom middleware (auth, logging, error handling)
│
│── services/               # Business logic (interacts with models, external APIs)
│
│── swagger/                # (Later) OpenAPI/Swagger documentation extensions
│
│── utils/                  # Shared helpers (security, hashing, token management)
│   └── __init__.py
│
│── vector/                  # Handles vector storage and access
│
│── app.py                  # FastAPI application factory
│── server.py               # Entry point (runs the app with uvicorn/gunicorn)
│
tests/                      # Unit & integration tests
```

## Layered Architecture

The project adheres to 3-tier architecture with a clean separation of concerns.

| Layer          | Responsibility                                                                                                                                              |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Model**      | Defines data structures and database models (SQLModel ORM + Pydantic schemas). Handles data persistence logic through DataModel classes.                    |
| **Service**    | Contains business rules and domain logic. Interacts with Models, enforces <br/> constraints (e.g., token limits, document caps), and coordinates workflows. |
| **Controller** | Orchestrates services in response to API requests. Maps request/response to schemas, handles errors, and returns standardized responses.                    |

## Authentication & Authorization

- JWT-based authentication (access & refresh tokens).

- Middleware ensures protected endpoints require authentication.

- Role-based access can be extended (e.g., user, admin).

## Database Design

- SQLModel (PostgresSQL backend).

- Entities: User, ChatSession, Document, ChatMessage, UsageStats.

- Each has its own DataModel class inside database/models to encapsulate CRUD operations.

- Schema (Pydantic) classes are defined in database/schemas for request/response validation.

## Data Flow

1. Request enters via route → Mapped in api/v1/routes.

2. Controller layer validates input, orchestrates services, and manages error handling.

3. Service layer performs business logic (e.g., verifying token quota, calling RAG pipeline).

4. Model/Data layer performs DB operations and returns results.

5. Controller returns the response wrapped in standardized JSON schema.

### Example Flow: Creating a Chat Session

1. Route: POST /sessions/

2. Controller: SessionController.create_session()

3. Service: SessionService.create_session(user, data) → validates user plan/quota.

4. Model: ChatSessionModel.create(data) → inserts into DB.

5. Response: New session details (via schema) returned to the client.

## (Basic) Middleware Responsibilities

- Authentication middleware: validates JWT tokens.

- Error handling middleware: converts unhandled exceptions into proper HTTP responses.

- Logging middleware: captures request/response cycles for debugging & monitoring.

## Modularity & Extensibility

- Each domain (User, Session, Document, Message, Usage) has its own Service + Controller + DataModel.

- Adding new features (e.g., payment plans, analytics) requires minimal changes due to modular design.

- Database repository pattern allows easy migration from Postgres → MySQL → SQLite if needed.

## Testing Strategy

- Unit tests: For services and models.

- Integration tests: For API endpoints (via FastAPI TestClient).

- Mocking external dependencies: (e.g., vector DB, RAG pipeline).

