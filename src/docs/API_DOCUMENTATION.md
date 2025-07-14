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

---

## 🔗 API Endpoints


### 🧾 Auth & User

| Method | Endpoint         | Description                                  |
|--------|------------------|----------------------------------------------|
| POST   | `/auth/register` | Register a new user                          |
| POST   | `/auth/login`    | Authenticate and receive JWT                 |
| GET    | `/auth/me`       | Get current user details                     |
| POST   | `/auth/logout`   | Log out user (optional token blacklist)      |
| PATCH  | `/auth/update`   | Update user info (email, password, etc.)     |
| GET    | `/auth/usage`    | Show token/doc upload usage for current user |


### 💬 Chatbot Sessions

| Method | Endpoint         | Description                             |
|--------|------------------|-----------------------------------------|
| GET    | `/sessions/`     | List all sessions for current user      |
| POST   | `/sessions/`     | Create a new chatbot session            |
| GET    | `/sessions/{id}` | Get details of a specific session       |
| DELETE | `/sessions/{id}` | Delete a session and associated content |
| PATCH  | `/sessions/{id}` | Rename or describe session              |


### 📄 Document Management

| Method | Endpoint                       | Description                               |
|--------|--------------------------------|-------------------------------------------|
| POST   | `/sessions/{id}/upload`        | Upload one or more documents to a session |
| GET    | `/sessions/{id}/documents`     | Get all documents in a session            |
| GET    | `/documents/{doc_id}/download` | Download original document                |
| DELETE | `/documents/{doc_id}`          | Delete a document from a session          |


### 🤖 Chat Interaction

| Method | Endpoint                  | Description                                |
|--------|---------------------------|--------------------------------------------|
| POST   | `/sessions/{id}/chat`     | Ask a question to the chatbot              |
| GET    | `/sessions/{id}/messages` | List chat messages from a session          |
| GET    | `/messages/{message_id}`  | View single chat message (metadata/answer) |


### 📤 Export & Download

| Method | Endpoint                    | Description                     |
|--------|-----------------------------|---------------------------------|
| GET    | `/sessions/{id}/export/pdf` | Export chat history as PDF      |
| GET    | `/sessions/{id}/export/txt` | Export chat history as TXT file |


### 🔍 Search

| Method | Endpoint                     | Description                    |
| ------ | ---------------------------- | ------------------------------ |
| GET    | `/search/sessions?q=keyword` | Search session titles or notes |
| GET    | `/search/messages?q=keyword` | Search through message content |


### 📊 Dashboard & Usage

| Method | Endpoint             | Description                               |
| ------ | -------------------- | ----------------------------------------- |
| GET    | `/dashboard/summary` | Summary of usage (sessions, tokens, etc.) |
| GET    | `/dashboard/tokens`  | Token usage logs (daily, weekly, etc.)    |
| GET    | `/dashboard/limits`  | Current plan limits and quotas            |


### 🛠️ Admin (Optional)

| Method | Endpoint                | Description                            |
| ------ | ----------------------- | -------------------------------------- |
| GET    | `/admin/users`          | View all registered users (admin only) |
| GET    | `/admin/stats`          | View overall platform statistics       |
| POST   | `/admin/users/{id}/ban` | Disable user account                   |

