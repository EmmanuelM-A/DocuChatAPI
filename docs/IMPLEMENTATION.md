# Implementation Plan

This document outlines the step-by-step implementation plan for the **DocuChatAPI** project.  
It details the order of implementation, testing scope, and important considerations for each milestone.  

---

## 1. High-Level Roadmap

| Phase   | Task Group                    | Priority   | Description                                                                                         |
|---------|-------------------------------|------------|-----------------------------------------------------------------------------------------------------|
| 1       | Project Setup                 | High       | Initialize FastAPI project, configure environment, database connection, and base project structure. |
| 2       | Core API Setup                | High       | Expose RAG chatbot functionality via REST API with initial endpoints.                               |
| 3       | User Management               | High       | Implement user authentication/authorization (JWT), registration, and login.                         |
| 4       | Session & Document Management | High       | Add support for sessions, document uploads, embeddings storage, and metadata management.            |
| 5       | Chat Messaging                | High       | Enable chat persistence, roles, and history retrieval.                                              |
| 6       | Usage Tracking                | Medium     | Track token usage, doc count, and session count per user.                                           |
| 7       | Testing & QA                  | High       | Implement unit, integration, and e2e tests progressively.                                           |
| 8       | Advanced Features             | Medium     | Rate limiting, middleware (logging, error handling), plan enforcement (free vs premium).            |
| 9       | Deployment                    | High       | Dockerize, configure CI/CD, setup production database/vector store.                                 |

---

## 2. Step-by-Step Implementation Plan

### Phase 1: Project Setup
- Initialize FastAPI project structure (3-tier: Models → Services → Controllers).
- Configure PostgresSQL connection using `sqlmodel`.
- Create base `DatabaseConnection` class.
- Set up `.env` handling with `pydantic-settings`.
- Add Docker support for local development (Postgres + API).
- Configure OpenAPI docs auto-generation (Swagger UI).

**Testing**:  
- Unit: DB connection, health check endpoint.  
- Integration: API startup and DB migrations.

---

### Phase 2: Core API Setup (RAG Chatbot)
- Convert existing RAG chatbot into a service layer (`rag_service.py`).  
- Implement base controller & route for chatbot query:  
  - `/chat/query` (accepts user message, returns response).  
- Store/retrieve vectors locally first (pickle/FAISS).  

**Testing**:  
- Unit: Mock vector retrieval + LLM response.  
- Integration: Full query pipeline test with fake docs.  
- E2E: One user asks → API returns coherent response.

---

### Phase 3: User Management
- Define `User` SQLModel.  
- Implement CRUD for user creation, find by email/username.  
- Secure password hashing with `bcrypt`.  
- Implement JWT authentication (`/auth/register`, `/auth/login`, `/auth/me`).  
- Middleware for user authentication.  

**Testing**:  
- Unit: Password hashing, token encoding/decoding.  
- Integration: Register → login → get user profile.  
- E2E: Full user onboarding flow.  

---

### Phase 4: Session & Document Management
- Define `ChatSession` and `Document` models.  
- Session service: create, list, delete sessions per user.  
- Document service: upload, store metadata, and embed content.  
- Store embeddings in FAISS (local for dev, remote in prod).  
- Link documents to sessions & users.  

**Testing**:  
- Unit: CRUD functions for session/doc.  
- Integration: Upload doc → store vectors → retrieve metadata.  
- E2E: Full flow — user uploads doc and starts session.  

---

### Phase 5: Chat Messaging
- Define `ChatMessage` model.  
- Service for storing chat history (user + assistant messages).  
- Retrieve full session history endpoint.  

**Testing**:  
- Unit: Message creation, token count calculation.  
- Integration: Query → response → persisted message.  
- E2E: User can retrieve session history after multiple chats.  

---

### Phase 6: Usage Tracking
- Define `UsageStats` model.  
- Increment token count on every chat.  
- Update doc count/session count on creation.  
- Expose endpoint `/users/{id}/usage`.  

**Testing**:  
- Unit: Usage update functions.  
- Integration: Chat triggers token count increment.  
- E2E: User dashboard usage retrieved correctly.  

---

### Phase 7: Testing & QA
- Consolidate all test layers.  
- Ensure coverage of ≥ 70% on service layer.  
- Run regression suite on CI/CD.  

**Testing Scope**:  
- Unit: Every service and utility function.  
- Integration: Endpoints covering flows.  
- E2E: Main workflows (register → upload doc → chat → retrieve stats).  

---

### Phase 8: Advanced Features (Optional for MVP)
- Middleware for request logging & error handling.  
- Rate limiting (per plan).  
- API key support for external integrations.  
- Admin endpoints for managing users/docs/sessions.  

**Testing**:  
- Unit: Middleware error handling.  
- Integration: Rate limiting logic.  

---

### Phase 9: Deployment
- Dockerize API + Postgres + Vector DB.  
- Setup GitHub Actions (CI/CD).  
- Deploy to cloud (e.g., AWS ECS, GCP Cloud Run, or Azure).  
- Configure production vector storage (Postgres HNSW/pgvector or Pinecone).  

**Testing**:  
- E2E: Run smoke tests post-deployment.  
- Performance: Load test on production-like setup.  

---

## 3. Implementation Priorities

| Order   | Component            | Why First?                                                          |
|---------|----------------------|---------------------------------------------------------------------|
| 1       | Core API Setup (RAG) | Already implemented, just needs API exposure. Establishes backbone. |
| 2       | User Management      | Needed for multi-user system and authentication.                    |
| 3       | Sessions + Documents | Enables document-based context for chatbot.                         |
| 4       | Chat Messaging       | Completes conversational loop with persistence.                     |
| 5       | Usage Stats          | Adds tracking for plans/limits.                                     |
| 6       | Advanced Features    | Nice-to-have polish after MVP.                                      |
| 7       | Deployment           | Prepares system for real-world usage.                               |

---

## 4. Final Deliverables

- **MVP**: User auth, RAG chatbot, sessions, docs, basic usage tracking.  
- **Post-MVP**: Admin tools, rate limits, premium plan features.  
- **Deployment**: Production-ready Dockerized system with CI/CD.

---

## 5. Suggested Timeline (Gantt-style Plan)

This is a **6-week roadmap** for implementing the project from core RAG → API → deployment.  
You can extend or shorten depending on available time and resources.

| Week       | Milestones                 | Tasks                                                                                                                                                          | Testing Focus                                                                                   |
|------------|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| **Week 1** | **Project Setup**          | - Initialize FastAPI project <br> - Setup database connection & migrations <br> - Configure Docker for Postgres + API <br> - Base health check route           | Unit: DB connection <br> Integration: API startup                                               |
| **Week 2** | **Core API (RAG)**         | - Wrap existing RAG chatbot logic in service layer <br> - Implement `/chat/query` endpoint <br> - Add basic request validation <br> - Local FAISS vector store | Unit: RAG service mock tests <br> Integration: query pipeline <br> E2E: chatbot response        |
| **Week 3** | **User Management**        | - User model (SQLModel) <br> - Auth service (hashing, JWT) <br> - `/auth/register`, `/auth/login`, `/auth/me` <br> - Middleware for auth                       | Unit: password & token utils <br> Integration: register → login <br> E2E: user onboarding       |
| **Week 4** | **Sessions & Documents**   | - Models for `ChatSession` & `Document` <br> - Upload + metadata storage <br> - Embedding + FAISS insert <br> - Session CRUD endpoints                         | Unit: doc/session repo tests <br> Integration: doc upload pipeline <br> E2E: upload → query     |
| **Week 5** | **Chat Messaging & Usage** | - Chat history persistence <br> - Session history retrieval <br> - Usage stats per user (tokens/docs/sessions) <br> - `/users/{id}/usage`                      | Unit: message persistence <br> Integration: chat history retrieval <br> E2E: multi-turn session |
| **Week 6** | **Polish & Deployment**    | - Add logging/error middleware <br> - Rate limiting (optional) <br> - Dockerize full stack <br> - Setup CI/CD <br> - Deploy to cloud                           | Unit: middleware logic <br> Integration: CI/CD pipeline <br> E2E: smoke tests in prod           |

---

## 6. Dependencies Between Phases

1. **Core API (Week 2)** depends on **Setup (Week 1)**.  
2. **User Management (Week 3)** must be in place before **Sessions/Documents (Week 4)**.  
3. **Chat Messaging & Usage (Week 5)** depend on **Sessions/Documents (Week 4)**.  
4. **Deployment (Week 6)** requires all other phases to be working.  

---

## 7. Deliverables Per Week

- **Week 1**: API skeleton, DB up and running.  
- **Week 2**: RAG accessible via API (first working chatbot endpoint).  
- **Week 3**: Secure multi-user system.  
- **Week 4**: Users can upload documents & start sessions.  
- **Week 5**: Users can chat in sessions and view usage stats.  
- **Week 6**: Production-ready system, CI/CD, cloud deployment.  
