## 🗄️ Database Models Overview

### 🔐 User

```cmd
User {
    id: UUID
    username: str
    email: str
    hashed_password: str
    plan: str  # free
    total_tokens_used: int
    created_at: datetime
}
```

### 💬 Session

```cmd
ChatSession {
    id: UUID
    user_id: FK
    title: str
    description: str
    created_at: datetime
}
```

### 📎 Document

```cmd
Document {
    id: UUID
    session_id: FK -> ChatSession
    user_id: FK -> User
    filename: str
    content: text
    vector_id: str
    tokens_used: int
    created_at: datetime
}
```

### 💬 Message

```cmd
ChatMessage {
    id: UUID
    session_id: FK
    user_id: FK
    role: enum (user, assistant)
    content: text
    token_count: int
    created_at: datetime
}
```

### 📊 Usage Stats

```cmd
UsageStats {
    id: UUID
    user_id: FK
    daily_token_count: int
    doc_count: int
    session_count: int
}
```
