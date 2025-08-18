# API Specification

## API Endpoints

This document outlines the API endpoints for the DocuChat API, categorized by feature 
domain. All routes are prefixed with `/api/v1/`.

### 🧾 Auth

| Method | Endpoint         | Description                                  |
|--------|------------------|----------------------------------------------|
| POST   | `/auth/register` | Register a new user                          |
| POST   | `/auth/login`    | Authenticate and receive JWT                 |
| POST   | `/auth/logout`   | Log out user (optional token blacklist)      |

### 🧾 User

| Method | Endpoint       | Description                                  |
|--------|----------------|----------------------------------------------|
| GET    | `/user/me`     | Get current user details                     |
| PATCH  | `/user/update` | Update user info (email, password, etc.)     |
| GET    | `/user/usage`  | Show token/doc upload usage for current user |

### 💬 Chatbot Sessions

| Method | Endpoint         | Description                             |
|--------|------------------|-----------------------------------------|
| GET    | `/sessions/`     | List all sessions for current user      |
| POST   | `/sessions/`     | Create a new chatbot session            |
| GET    | `/sessions/{id}` | Get details of a specific session       |
| DELETE | `/sessions/{id}` | Delete a session and associated content |
| PATCH  | `/sessions/{id}` | Update session details                  |


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
|--------|------------------------------|--------------------------------|
| GET    | `/search/sessions?q=keyword` | Search session titles or notes |
| GET    | `/search/messages?q=keyword` | Search through message content |


### 📊 Dashboard & Usage

| Method | Endpoint             | Description                               |
|--------|----------------------|-------------------------------------------|
| GET    | `/dashboard/summary` | Summary of usage (sessions, tokens, etc.) |
| GET    | `/dashboard/tokens`  | Token usage logs (daily, weekly, etc.)    |
| GET    | `/dashboard/limits`  | Current plan limits and quotas            |


### 🛠️ Admin (Optional)

| Method | Endpoint                | Description                            |
|--------|-------------------------|----------------------------------------|
| GET    | `/admin/users`          | View all registered users (admin only) |
| GET    | `/admin/stats`          | View overall platform statistics       |
| POST   | `/admin/users/{id}/ban` | Disable user account                   |
