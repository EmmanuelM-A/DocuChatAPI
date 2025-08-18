# Project Architecture – DocuChatAPI

---

## Overview

The **DocuChatAPI** is a modular **FastAPI-based Retrieval-Augmented Generation 
(RAG) backend** designed to support user-managed chatbot sessions, document uploads, 
and conversational interactions with vector-based retrieval.  

The system follows a **layered architecture**:

- **API Layer** → Handles HTTP requests/responses.

- **Service Layer** → Encapsulates business logic (sessions, documents, messaging). 

- **Persistence Layer** → Manages database storage and vector embeddings. 

- **AI Layer** → RAG pipeline (retrieval + LLM response).

## High-Level Architecture

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

## Component Breakdown

### 🔹 API Layer

- **Routers** for `auth`, `users`, `sessions`, `documents`, `messages`, `usage`.  
- **Dependencies**: Database session injection, authentication guards.  

### 🔹 Service Layer

- **Session Service** – Creates chat sessions, enforces limits, retrieves history.  
- **Document Service** – Handles file ingestion, text chunking, vector embedding.  
- **Message Service** – Stores and retrieves chat messages.  
- **Usage Service** – Tracks token usage, session count, and uploads.  

### 🔹 Persistence Layer

- **SQLModel ORM** – Defines relational schemas (`User`, `ChatSession`, `Document`, 
`ChatMessage`, `UsageStats`).

- **CRUD Operations** – Encapsulated per schema (e.g., `user_model.py`, `session_model.py`).  

- **Vector Store Integration** – Maintains embeddings and supports similarity search.  

### 🔹 AI Layer

- **RAG Pipeline:**

  1. Retrieve top-k relevant document chunks.  
  2. Construct prompt with context + chat history.  
  3. Call LLM (OpenAI API, HuggingFace, or custom).  
  4. Stream or return assistant response.

- **User** – Auth + subscription details.  

- **ChatSession** – Groups related documents and messages.

- **Document** – Uploads linked to sessions & users.

- **ChatMessage** – Logs conversations (user ↔ assistant). 

- **UsageStats** – Tracks token usage and limits.

## Suggested Diagrams to Draw

### High-Level System Diagram

- Shows: API Layer → Service Layer → Persistence Layer → AI Layer → LLM.

- Request flow: **User → FastAPI → DB + Vector Store → LLM → Response**.  

### Database ER Diagram

- Entities: `User`, `ChatSession`, `Document`, `ChatMessage`, `UsageStats`.  
- Relationships:  
  - `User (1) → (∞) ChatSession`  
  - `ChatSession (1) → (∞) Document`  
  - `ChatSession (1) → (∞) ChatMessage`  
  - `User (1) → (1) UsageStats`  

### Sequence Diagram (Chat Request Flow)

1. User sends message.  
2. API validates authentication.  
3. Retrieve session + documents from DB/vector store.  
4. Construct RAG prompt → Send to LLM.  
5. Receive assistant response.  
6. Store message + tokens in DB.  
7. Return response to user.  

---

## Scalability & Extension Points

- **Pluggable Vector Store**: Start with FAISS (local), upgrade to Pinecone/Weaviate.  
- **Authentication**: OAuth2/JWT, extendable for enterprise SSO.  
- **Task Queues** (Celery, RQ) for background document ingestion.  
- **Caching Layer** (Redis) for faster retrieval & token savings.
