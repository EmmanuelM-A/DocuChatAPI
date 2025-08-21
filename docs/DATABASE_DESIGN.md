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

### 🏷️ `Plan`

Stores the plan data

| Column              | Type        | Constraints      | Purpose                           |
|---------------------|-------------|------------------|-----------------------------------|
| `id`                | UUID (PK)   | Primary Key      | Unique plan identifier            |
| `name`              | VARCHAR(50) | Unique, Not Null | Plan name (free, pro, enterprise) |
| `token_limit_daily` | INT         | Not Null         | Daily token allowance             |
| `document_limit`    | INT         | Not Null         | Max documents per session         |
| `session_limit`     | INT         | Not Null         | Max concurrent sessions           |
| `price_monthly`     | DECIMAL     | Default = 0.00   | Monthly cost                      |
| `is_active`         | BOOLEAN     | Default = true   | Whether plan is available         |
| `created_at`        | TIMESTAMP   | Default = now()  | Plan creation time                |

### 🔐 `User`

Stores user account information.

| Column              | Type         | Constraints                     | Purpose                   |
|---------------------|--------------|---------------------------------|---------------------------|
| `id`                | UUID (PK)    | Primary Key                     | Unique identifier         |
| `username`          | VARCHAR(50)  | Unique, Not Null                | Username for login        |
| `email`             | VARCHAR(255) | Unique, Not Null                | Email for authentication  |
| `hashed_password`   | VARCHAR(255) | Not Null                        | Securely stored password  |
| `plan_id`           | UUID (FK)    | References `Plan(id)`, Not Null | Current subscription      |
| `total_tokens_used` | BIGINT       | Default = 0                     | Lifetime token usage      |
| `is_active`         | BOOLEAN      | Default = true                  | Account status            |
| `email_verified`    | BOOLEAN      | Default = false                 | Email verification status |
| `last_login_at`     | TIMESTAMP    | Nullable                        | Last successful login     |
| `created_at`        | TIMESTAMP    | Default = now()                 | Account creation          |
| `updated_at`        | TIMESTAMP    | Default = now()                 | Last modification         |

### 💬 `ChatSession`

Represents a logical conversation between the user and the assistant.

| Column             | Type         | Constraints                             | Purpose                              |
|--------------------|--------------|-----------------------------------------|--------------------------------------|
| `id`               | UUID (PK)    | Primary Key                             | Unique session identifier            |
| `user_id`          | UUID (FK)    | References `User(id)` ON DELETE CASCADE | Session owner                        |
| `title`            | VARCHAR(255) | Nullable                                | User-defined or auto-generated title |
| `description`      | TEXT         | Nullable                                | Session description                  |
| `total_messages`   | INT          | Default = 0                             | Cached message count                 |
| `total_tokens`     | INT          | Default = 0                             | Cached token usage for session       |
| `created_at`       | TIMESTAMP    | Default = now()                         | Session start                        |
| `updated_at`       | TIMESTAMP    | Default = now()                         | Last modification                    |

### 📎 `Document`

Holds user-uploaded documents that are linked to sessions and embedded for retrieval.

| Column              | Type         | Constraints                                    | Purpose                              |
|---------------------|--------------|------------------------------------------------|--------------------------------------|
| `id`                | UUID (PK)    | Primary Key                                    | Unique document identifier           |
| `session_id`        | UUID (FK)    | References `ChatSession(id)` ON DELETE CASCADE | Parent session                       |
| `user_id`           | UUID (FK)    | References `User(id)` ON DELETE CASCADE        | Document owner                       |
| `filename`          | VARCHAR(255) | Not Null                                       | Original filename                    |
| `file_size`         | BIGINT       | Not Null                                       | File size in bytes                   |
| `mime_type`         | VARCHAR(100) | Not Null                                       | File MIME type                       |
| `content`           | TEXT         | Not Null                                       | Extracted text content               |
| `content_hash`      | VARCHAR(64)  | Not Null                                       | SHA-256 of content for deduplication |
| `vector_id`         | VARCHAR(255) | Nullable                                       | Vector store reference               |
| `embedding_model`   | VARCHAR(100) | Nullable                                       | Model used for embeddings            |
| `tokens_used`       | INT          | Default = 0                                    | Tokens for processing                |
| `processing_status` | ENUM         | Values: pending, processing, completed, failed | Processing state                     |
| `error_message`     | TEXT         | Nullable                                       | Error details if processing failed   |
| `created_at`        | TIMESTAMP    | Default = now()                                | Upload time                          |
| `updated_at`        | TIMESTAMP    | Default = now()                                | Last modification                    |

### 💬 `ChatMessage`

Logs all conversation messages exchanged in a session.

| Column               | Type         | Constraints                                     | Purpose                         |
|----------------------|--------------|-------------------------------------------------|---------------------------------|
| `id`                 | UUID (PK)    | Primary Key                                     | Unique message identifier       |
| `session_id`         | UUID (FK)    | References `ChatSession(id)` ON DELETE CASCADE  | Parent session                  |
| `user_id`            | UUID (FK)    | References `User(id)` ON DELETE SET NULL        | Message author                  |
| `parent_message_id`  | UUID (FK)    | References `ChatMessage(id)` ON DELETE SET NULL | For threaded conversations      |
| `role`               | ENUM         | Values: user, assistant, system                 | Message type                    |
| `content`            | TEXT         | Not Null                                        | Message content                 |
| `token_count`        | INT          | Default = 0                                     | Tokens in this message          |
| `model_used`         | VARCHAR(100) | Nullable                                        | AI model for assistant messages |
| `context_documents`  | JSON         | Nullable                                        | Document IDs used for RAG       |
| `processing_time_ms` | INT          | Nullable                                        | Response generation time        |
| `created_at`         | TIMESTAMP    | Default = now()                                 | Message timestamp               |
| `updated_at`         | TIMESTAMP    | Default = now()                                 | Last modification               |

### 📊 `UsageStats`

Tracks aggregate statistics for each user.

| Column               | Type      | Constraints                             | Purpose                     |
|----------------------|-----------|-----------------------------------------|-----------------------------|
| `id`                 | UUID (PK) | Primary Key                             | Unique record ID            |
| `user_id`            | UUID (FK) | References `User(id)` ON DELETE CASCADE | Stats owner                 |
| `date`               | DATE      | Not Null                                | Stats date                  |
| `tokens_used`        | INT       | Default = 0                             | Tokens consumed this day    |
| `messages_sent`      | INT       | Default = 0                             | Messages sent this day      |
| `documents_uploaded` | INT       | Default = 0                             | Documents uploaded this day |
| `sessions_created`   | INT       | Default = 0                             | Sessions created this day   |
| `created_at`         | TIMESTAMP | Default = now()                         | Record creation             |
| `updated_at`         | TIMESTAMP | Default = now()                         | Last update                 |

### 🔍 `DocumentChunk`

For better RAG performance with large documents

| Column           | Type         | Constraints                                 | Purpose                     |
|------------------|--------------|---------------------------------------------|-----------------------------|
| `id`             | UUID (PK)    | Primary Key                                 | Unique chunk identifier     |
| `document_id`    | UUID (FK)    | References `Document(id)` ON DELETE CASCADE | Parent document             |
| `chunk_index`    | INT          | Not Null                                    | Order within document       |
| `content`        | TEXT         | Not Null                                    | Chunk text content          |
| `vector_id`      | VARCHAR(255) | Nullable                                    | Vector store reference      |
| `token_count`    | INT          | Default = 0                                 | Tokens in chunk             |
| `start_position` | INT          | Not Null                                    | Character start in original |
| `end_position`   | INT          | Not Null                                    | Character end in original   |
| `created_at`     | TIMESTAMP    | Default = now()                             | Chunk creation              |


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

## Indexes for Performance

```sql
-- User indexes
CREATE INDEX idx_user_email ON User(email);
CREATE INDEX idx_user_plan_id ON User(plan_id);
CREATE INDEX idx_user_active ON User(is_active);

-- Session indexes
CREATE INDEX idx_session_user_id ON ChatSession(user_id);
CREATE INDEX idx_session_active ON ChatSession(is_active);
CREATE INDEX idx_session_last_activity ON ChatSession(last_activity_at);

-- Document indexes
CREATE INDEX idx_document_session_id ON Document(session_id);
CREATE INDEX idx_document_user_id ON Document(user_id);
CREATE INDEX idx_document_hash ON Document(content_hash);
CREATE INDEX idx_document_status ON Document(processing_status);

-- Message indexes
CREATE INDEX idx_message_session_id ON ChatMessage(session_id);
CREATE INDEX idx_message_user_id ON ChatMessage(user_id);
CREATE INDEX idx_message_created_at ON ChatMessage(created_at);
CREATE INDEX idx_message_parent ON ChatMessage(parent_message_id);

-- Usage stats indexes
CREATE INDEX idx_usage_user_date ON DailyUsageStats(user_id, date);
CREATE INDEX idx_usage_date ON DailyUsageStats(date);

-- Chunk indexes
CREATE INDEX idx_chunk_document_id ON DocumentChunk(document_id);
CREATE INDEX idx_chunk_vector_id ON DocumentChunk(vector_id);
```

## Deletion Cascading Rules

### When User is deleted:
- **ChatSession**: CASCADE (delete all sessions)
- **Document**: CASCADE (delete all documents)
- **ChatMessage**: SET NULL (preserve messages but remove user reference)
- **DailyUsageStats**: CASCADE (delete usage history)

### When ChatSession is deleted:
- **Document**: CASCADE (delete session documents)
- **ChatMessage**: CASCADE (delete conversation)

### When Document is deleted:
- **DocumentChunk**: CASCADE (delete all chunks)

### When Plan is deleted:
- **User**: RESTRICT (cannot delete plan with active users)

## Triggers for Data Consistency

```sql
-- Update session counters when messages change
CREATE TRIGGER update_session_stats_on_message
    AFTER INSERT ON ChatMessage
    FOR EACH ROW
    EXECUTE FUNCTION update_session_message_count();

-- Update user token totals
CREATE TRIGGER update_user_token_total
    AFTER INSERT OR UPDATE ON ChatMessage
    FOR EACH ROW
    EXECUTE FUNCTION update_user_total_tokens();

-- Update daily usage stats
CREATE TRIGGER update_daily_usage
    AFTER INSERT ON ChatMessage
    FOR EACH ROW
    EXECUTE FUNCTION update_daily_usage_stats();
```
