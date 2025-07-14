# AI-Powered Document Chatbot API Documentation

This is the official API documentation for the **AI-Powered Document Chatbot** 
web application built with FastAPI. The application allows users to upload 
documents, ask questions in natural language, and receive intelligent answers 
powered by RAG (Retrieval-Augmented Generation).

---

## 📌 Overview

### 🔥 Core Features

- JWT-based authentication
- Chatbot sessions for different use cases
- Document upload with file size & format validation
- Document embedding & vector search (via FAISS)
- Chat history per session
- PDF/text export of entire conversations
- Token usage tracking per user
- RESTful API with FastAPI and async tasks

---

## ⚙️ System Architecture

**Frontend:** React.js  
**Backend:** FastAPI (Python)  
**Database:** PostgresSQL (users, sessions, metadata)  
**Vector DB:** FAISS 
**Storage:** Local or Cloud (S3, etc.)  
**Auth:** JWT access & refresh tokens (cookie or header)  
**Background Tasks:** Celery / FastAPI tasks  
**LLM API:** OpenAI / Claude / Llama.cpp

---

## 📁 Project Structure

```cmd
src/
├── api/ # API routers (auth, sessions, chat, docs)
├── core/ # Configs, startup, security
├── models/ # Pydantic models (schemas)
├── db/ # SQLAlchemy models, sessions
├── services/ # Business logic (RAG, upload, chat)
├── utils/ # File, text, embedding utils
├── vectorstore/ # Embedding and similarity search logic
├── background/ # Async tasks (embedding, cleanup)
└── main.py # FastAPI app instance
```

---

## 🗄️ Database Models Overview

View database schemas [here]("./src/docs/DATABASE_SCHEMAS.md").


