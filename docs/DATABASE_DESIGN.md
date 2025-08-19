# Database Design - DocuChatAPI

## Overview

The database is a **relational model** designed to support the DocuChatAPI system.

It manages:
- Users and their authentication/subscription details.
- Chat sessions.
- Uploaded documents with embeddings.
- Messages exchanged between users and the assistant.
- Usage tracking for tokens, sessions, and documents.

## Tables

### 🔐 `User`

Stores user account information.

| Column              | Type       | Constraints                        | Purpose                                  |
|---------------------|------------|------------------------------------|------------------------------------------|
| `id`                | UUID (PK)  | Primary Key                        | Unique identifier for each user.         |
| `username`          | VARCHAR    | Unique, Not Null                   | Username for login/display.              |
| `email`             | VARCHAR    | Unique, Not Null                   | User’s email for authentication/contact. |
| `hashed_password`   | VARCHAR    | Not Null                           | Securely stored password.                |
| `plan`              | VARCHAR    | Default = "free"                   | User’s subscription tier.                |
| `total_tokens_used` | INT        | Default = 0                        | Running total of tokens consumed.        |
| `created_at`        | TIMESTAMP  | Default = now()                    | Account creation timestamp.              |
| `updated_at`        | TIMESTAMP  | Default = now()                    | Last update timestamp.                   |

### 💬 `ChatSession`

Represents a logical conversation between the user and the assistant.

| Column           | Type        | Constraints                      | Purpose                                   |
|------------------|-------------|----------------------------------|-------------------------------------------|
| `id`             | UUID (PK)   | Primary Key                      | Unique session identifier.                |
| `user_id`        | UUID (FK)   | References `User(id)`            | Owner of the session.                     |
| `title`          | VARCHAR     | Optional                         | Session title (user-defined or auto-set). |
| `description`    | TEXT        | Optional                         | Brief description of session purpose.     |
| `created_at`     | TIMESTAMP   | Default = now()                  | Timestamp of session creation.            |
| `updated_at`     | TIMESTAMP   | Default = now()                  | Last update timestamp.                    |

### 📎 `Document`

Holds user-uploaded documents that are linked to sessions and embedded for retrieval.

| Column        | Type      | Constraints                  | Purpose                              |
|---------------|-----------|------------------------------|--------------------------------------|
| `id`          | UUID (PK) | Primary Key                  | Unique identifier for each document. |
| `session_id`  | UUID (FK) | References `ChatSession(id)` | Links document to a session.         |
| `user_id`     | UUID (FK) | References `User(id)`        | Ensures document ownership.          |
| `filename`    | VARCHAR   | Not Null                     | Original file name.                  |
| `content`     | TEXT      | Not Null                     | Extracted raw text content.          |
| `vector_id`   | VARCHAR   | Optional                     | Reference to vector store embedding. |
| `tokens_used` | INT       | Default = 0                  | Tokens consumed during embedding.    |
| `created_at`  | TIMESTAMP | Default = now()              | Upload timestamp.                    |
| `updated_at`  | TIMESTAMP | Default = now()              | Last update timestamp.               |

### 💬 `ChatMessage`

Logs all conversation messages exchanged in a session.

| Column        | Type      | Constraints                    | Purpose                                    |
|---------------|-----------|--------------------------------|--------------------------------------------|
| `id`          | UUID (PK) | Primary Key                    | Unique identifier for each message.        |
| `session_id`  | UUID (FK) | References `ChatSession(id)`   | Belongs to a specific session.             |
| `user_id`     | UUID (FK) | References `User(id)`          | Author of the message (user or assistant). |
| `role`        | ENUM      | Values = {`user`, `assistant`} | Distinguishes between user and assistant.  |
| `content`     | TEXT      | Not Null                       | The actual message text.                   |
| `token_count` | INT       | Default = 0                    | Tokens consumed by this message.           |
| `created_at`  | TIMESTAMP | Default = now()                | Message timestamp.                         |
| `updated_at`  | TIMESTAMP | Default = now()                | Last update timestamp.                     |

### 📊 `UsageStats`

Tracks aggregate statistics for each user.

| Column              | Type      | Constraints           | Purpose                                 |
|---------------------|-----------|-----------------------|-----------------------------------------|
| `id`                | UUID (PK) | Primary Key           | Unique record ID.                       |
| `user_id`           | UUID (FK) | References `User(id)` | Stats are tracked per user.             |
| `daily_token_count` | INT       | Default = 0           | Tokens consumed per day (resets daily). |
| `doc_count`         | INT       | Default = 0           | Number of documents uploaded.           |
| `session_count`     | INT       | Default = 0           | Number of sessions created.             |
| `updated_at`        | TIMESTAMP | Default = now()       | Last update timestamp.                  |

## Relationships and Multiplicity

- **User → ChatSession**
  - One `User` can have many `ChatSessions`.  
  - **1-to-Many** (`User.id` → `ChatSession.user_id`).  

- **ChatSession → Document**  
  - One `ChatSession` can have many `Documents`.  
  - **1-to-Many** (`ChatSession.id` → `Document.session_id`).  

- **ChatSession → ChatMessage**  
  - One `ChatSession` can have many `ChatMessages`.  
  - **1-to-Many** (`ChatSession.id` → `ChatMessage.session_id`).  

- **User → Document**  
  - One `User` can upload many `Documents`.  
  - **1-to-Many** (`User.id` → `Document.user_id`).  

- **User → ChatMessage**  
  - One `User` can create many `ChatMessages`.  
  - **1-to-Many** (`User.id` → `ChatMessage.user_id`).  

- **User → UsageStats**  
  - One `User` has exactly one `UsageStats` record.  
  - **1-to-1** (`User.id` → `UsageStats.user_id`).


## Vector Database Design


### Local Development


### Production
