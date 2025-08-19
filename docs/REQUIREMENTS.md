# Requirements

This document defines the **requirements** for the DocuChatAPI project, including functional requirements (FR), non-functional requirements (NFR), and system constraints.  
The purpose of this document is to establish clear expectations for the system's capabilities, quality attributes, and limitations.

---

## 1. Functional Requirements (FR)

### 1.1 User Management
- **FR-1**: The system must allow users to register with email and password.  
- **FR-2**: The system must allow users to log in using JWT-based authentication.  
- **FR-3**: The system must allow users to log out and invalidate refresh tokens.  
- **FR-4**: The system must allow users to update their profile details (e.g., name, password).  
- **FR-5**: The system must allow users to delete their account and associated data.  

### 1.2 Document Management
- **FR-6**: Users must be able to upload documents (PDF, DOCX, TXT, MD).  
- **FR-7**: The system must extract text from uploaded documents and split them into chunks for embedding.  
- **FR-8**: The system must store document metadata (filename, type, size, owner, upload date).  
- **FR-9**: Users must be able to view their uploaded documents.  
- **FR-10**: Users must be able to delete previously uploaded documents.  

### 1.3 Vector Store Management
- **FR-11**: For each user, the system must create and maintain a vector store (FAISS index + metadata).  
- **FR-12**: Multiple chat sessions should be able to access the same user vector store.  
- **FR-13**: The system must support storing/retrieving embeddings associated with documents.  

### 1.4 Chat Sessions
- **FR-14**: Users must be able to create chat sessions.  
- **FR-15**: The system must retrieve relevant document chunks from the user’s vector store based on the query.  
- **FR-16**: The system must generate a response using an LLM with RAG (Retrieval-Augmented Generation).  
- **FR-17**: The system must store chat history for each session.  
- **FR-18**: Users must be able to view previous chat sessions and their messages.  

### 1.5 Usage & Limits
- **FR-19**: The system must track token usage per user.  
- **FR-20**: The system must enforce rate limits and plan-specific restrictions (e.g., free vs premium users).  

---

## 2. Non-Functional Requirements (NFR)

### 2.1 Performance
- **NFR-1**: The system should respond to API requests within **< 500ms** for non-LLM operations.  
- **NFR-2**: Vector similarity search should return results within **< 200ms** for a typical query.  
- **NFR-3**: The system should support at least **100 concurrent users** in the MVP phase.  

### 2.2 Scalability
- **NFR-4**: The system must be designed modularly (3-tier: Model → Service → Controller) for maintainability.  
- **NFR-5**: The system should support scaling horizontally using containers and orchestration (Kubernetes, Docker Compose).  
- **NFR-6**: Vector storage should be replaceable (local FAISS → external vector DB) without impacting APIs.  

### 2.3 Security
- **NFR-7**: All sensitive endpoints must be protected by JWT authentication.  
- **NFR-8**: Passwords must be hashed (e.g., bcrypt) before storage.  
- **NFR-9**: Communication must use HTTPS in production.  
- **NFR-10**: Uploaded documents must be accessible only by the owner.  

### 2.4 Reliability & Availability
- **NFR-11**: The system must provide **99.5% uptime** in production.  
- **NFR-12**: Failures in vector storage should not crash the API but return graceful errors.  
- **NFR-13**: All database writes must be atomic and consistent.  

### 2.5 Maintainability
- **NFR-14**: Code should follow common standards (PEP8, modular architecture, OOP principles).  
- **NFR-15**: Endpoint logic must be separated into testable components (Services, Controllers, Routes, Middleware).  
- **NFR-16**: Automated tests should cover at least **70% of core functionality**.  

### 2.6 Documentation
- **NFR-17**: All endpoints must be documented using Swagger/OpenAPI.  
- **NFR-18**: The project must include technical documentation (`ARCHITECTURE.md`, `DEPLOYMENT.md`, `DATABASE_DESIGN.md`, etc.).  

---

## 3. System Constraints

- **SC-1**: The system will use a **relational database (Postgres)** for core entities (users, sessions, documents, usage).  
- **SC-2**: The system will use **FAISS + Pickle metadata** for vector storage in MVP (local filesystem-based).  
- **SC-3**: A migration path to an external vector DB (Pinecone/Weaviate/Milvus) must be possible without breaking APIs.  
- **SC-4**: Only supported document types (PDF, DOCX, TXT, MD) are allowed in MVP.  
- **SC-5**: Maximum file size per upload: **20MB** (configurable).  
- **SC-6**: All deployments must be containerized (Docker).  
- **SC-7**: Secrets (API keys, DB credentials) must not be hardcoded but stored in environment variables.  
- **SC-8**: LLM integration (e.g., OpenAI API) requires internet access from the backend.  

---

## 4. Future Enhancements (Optional, Not MVP)

- Support for **multiple vector stores per user** (session-specific knowledge bases).  
- Integration with **cloud-native vector DB** (Pinecone, Weaviate, Milvus).  
- File type expansion (CSV, XLSX, images with OCR).  
- Real-time notifications and collaborative chat sessions.  
- Admin dashboard for monitoring usage and managing users.  

---
