# Frontend API Usage Guide - DocuChatAPI

## Overview

This guide outlines how a frontend application would interact with the DocuChatAPI to provide a complete user experience. The API follows REST principles with JWT authentication and provides comprehensive endpoints for document-based chat interactions.

---

## User Journey Flow

### 1. Authentication Flow

| Step | User Action                    | API Call                                | Frontend Response                       |
|------|--------------------------------|-----------------------------------------|-----------------------------------------|
| 1    | User visits registration page  | -                                       | Display registration form               |
| 2    | User submits registration form | `POST /api/v1/auth/register`            | Show success message, redirect to login |
| 3    | User submits login form        | `POST /api/v1/auth/login`               | Store JWT token, redirect to dashboard  |
| 4    | User accesses protected pages  | Include `Authorization: Bearer <token>` | Normal page access                      |
| 5    | Token expires                  | API returns 401                         | Redirect to login, clear stored token   |

**Frontend Implementation Considerations**:
- Store JWT token securely (httpOnly cookies or secure localStorage)
- Implement automatic token refresh if using refresh tokens
- Handle token expiration gracefully with user-friendly messages

---

## Core User Workflows

### 2. Session Management Workflow

| User Goal            | Frontend Flow                  | API Interactions                                                   | UI Elements                             |
|----------------------|--------------------------------|--------------------------------------------------------------------|-----------------------------------------|
| **View Sessions**    | Dashboard loads                | `GET /api/v1/sessions/`                                            | Session list with titles, last activity |
| **Create Session**   | Click "New Chat" → Enter title | `POST /api/v1/sessions/`                                           | Modal dialog → redirect to chat         |
| **Continue Session** | Click existing session         | `GET /api/v1/sessions/{id}` + `GET /api/v1/sessions/{id}/messages` | Load chat interface with history        |
| **Delete Session**   | Click delete → confirm         | `DELETE /api/v1/sessions/{id}`                                     | Remove from list, show confirmation     |

**Frontend State Management**:
- Maintain list of user sessions
- Cache session metadata for quick navigation
- Update session "last activity" on interaction

### 3. Document Upload & Management

| User Action            | Frontend Behavior      | API Sequence                          | User Feedback                                    |
|------------------------|------------------------|---------------------------------------|--------------------------------------------------|
| **Select Files**       | File picker dialog     | -                                     | Show selected file names and sizes               |
| **Upload Documents**   | Progress indicator     | `POST /api/v1/sessions/{id}/upload`   | Upload progress bar                              |
| **Monitor Processing** | Poll processing status | `GET /api/v1/sessions/{id}/documents` | Status indicators (pending/processing/completed) |
| **View Documents**     | Document list panel    | `GET /api/v1/sessions/{id}/documents` | File names, upload dates, processing status      |
| **Delete Document**    | Confirmation dialog    | `DELETE /api/v1/documents/{doc_id}`   | Remove from list, update chat context            |

**Processing Status Handling**:

| Status       | Frontend Display            | User Actions        | Polling Strategy     |
|--------------|-----------------------------|---------------------|----------------------|
| `pending`    | "Queued for processing"     | Wait                | Poll every 5 seconds |
| `processing` | "Processing document..."    | Wait                | Poll every 3 seconds |
| `completed`  | "Ready for chat"            | Can start chatting  | Stop polling         |
| `failed`     | "Processing failed" + error | Retry upload option | Show error details   |

### 4. Chat Interaction Workflow

| Chat Phase                | User Interaction                 | API Call                          | Frontend Updates                                  |
|---------------------------|----------------------------------|-----------------------------------|---------------------------------------------------|
| **Send Message**          | Type message → press send        | `POST /api/v1/sessions/{id}/chat` | Add user message to chat, show "typing" indicator |
| **Receive Response**      | Wait for response                | Response from chat endpoint       | Add assistant message, hide typing indicator      |
| **View Sources**          | Click "View Sources" on response | Metadata from chat response       | Show document excerpts used                       |
| **Continue Conversation** | Send follow-up message           | `POST /api/v1/sessions/{id}/chat` | Maintain conversation context                     |

**Real-time UX Considerations**:
- Show typing indicators during API processing
- Stream responses if API supports it (future enhancement)
- Display token usage in real-time
- Show document context used for each response

---

## Dashboard & Analytics Interface

### 5. User Dashboard Components

| Component             | Data Source                     | Update Frequency | User Value                       |
|-----------------------|---------------------------------|------------------|----------------------------------|
| **Usage Summary**     | `GET /api/v1/dashboard/summary` | On page load     | Current usage vs limits          |
| **Token Usage Chart** | `GET /api/v1/dashboard/tokens`  | Daily            | Visual usage patterns            |
| **Recent Sessions**   | `GET /api/v1/sessions/?limit=5` | On page load     | Quick access to recent chats     |
| **Plan Details**      | `GET /api/v1/dashboard/limits`  | On page load     | Current plan and upgrade options |

### 6. Usage Tracking Display

| Metric                 | API Endpoint              | Display Format               | Warning Triggers       |
|------------------------|---------------------------|------------------------------|------------------------|
| **Daily Tokens**       | `/dashboard/tokens`       | Progress bar with percentage | 80% usage warning      |
| **Documents Uploaded** | `/user/usage`             | Count with session breakdown | Approaching limit      |
| **Sessions Created**   | `/dashboard/summary`      | Count with creation dates    | Limit reached          |
| **Storage Used**       | Calculated from documents | MB/GB with visual indicator  | Storage quota warnings |

---

## Advanced Features Integration

### 7. Search Functionality

| Search Type        | User Interface             | API Integration                         | Results Display             |
|--------------------|----------------------------|-----------------------------------------|-----------------------------|
| **Session Search** | Search bar on dashboard    | `GET /api/v1/search/sessions?q=keyword` | Filtered session list       |
| **Message Search** | Search within chat history | `GET /api/v1/search/messages?q=keyword` | Highlighted message results |
| **Global Search**  | Unified search interface   | Combined API calls                      | Categorized results         |

### 8. Export & Sharing Features

| Export Type       | Trigger                 | API Call                               | User Experience        |
|-------------------|-------------------------|----------------------------------------|------------------------|
| **PDF Export**    | "Export as PDF" button  | `GET /api/v1/sessions/{id}/export/pdf` | Download dialog        |
| **Text Export**   | "Export as Text" button | `GET /api/v1/sessions/{id}/export/txt` | Download dialog        |
| **Share Session** | "Share" button (future) | Generate share link                    | Copy link to clipboard |

---

## Error Handling & User Experience

### 9. Error States & Recovery

| Error Type                | User Experience                 | Recovery Actions               | Prevention                   |
|---------------------------|---------------------------------|--------------------------------|------------------------------|
| **Authentication Errors** | Redirect to login with message  | Re-authenticate                | Token refresh implementation |
| **Upload Failures**       | Retry option with error details | Manual retry or different file | File validation              |
| **Chat Failures**         | "Failed to send" with retry     | Retry button                   | Connection status indicator  |
| **Quota Exceeded**        | Clear upgrade prompt            | Plan upgrade or wait           | Real-time usage tracking     |

### 10. Loading States & Performance

| Operation           | Loading Indicator            | Timeout Handling     | Performance Optimization |
|---------------------|------------------------------|----------------------|--------------------------|
| **Document Upload** | Progress bar with percentage | Cancel upload option | Chunked upload           |
| **Chat Response**   | Typing indicator with dots   | Timeout after 30s    | Response streaming       |
| **Session Loading** | Skeleton UI for messages     | Retry mechanism      | Message pagination       |
| **Dashboard Data**  | Loading spinners             | Cached data display  | Background refresh       |

---

## Mobile Responsiveness Considerations

### 11. Mobile-Specific UX

| Feature                | Desktop Experience        | Mobile Adaptation           | Technical Notes            |
|------------------------|---------------------------|-----------------------------|----------------------------|
| **File Upload**        | Drag & drop + file picker | Camera option + file picker | Accept camera images       |
| **Chat Interface**     | Side-by-side layout       | Full-screen chat            | Collapsible document panel |
| **Document View**      | Inline preview            | Modal overlay               | Touch-friendly navigation  |
| **Session Management** | List view                 | Swipe actions               | Pull-to-refresh            |

---

## API Integration Patterns

### 12. Frontend Architecture Recommendations

| Pattern                | Use Case                     | Implementation                     | Benefits                     |
|------------------------|------------------------------|------------------------------------|------------------------------|
| **Service Layer**      | All API calls                | Centralized HTTP client            | Consistent error handling    |
| **State Management**   | User data, sessions          | Vuex/Redux/Context API             | Reactive UI updates          |
| **Caching Strategy**   | Session list, user profile   | Local storage + cache invalidation | Improved performance         |
| **Optimistic Updates** | Message sending, file upload | Update UI before API confirmation  | Better perceived performance |

### 13. Security Considerations

| Security Aspect             | Frontend Implementation  | API Dependency         | User Impact                |
|-----------------------------|--------------------------|------------------------|----------------------------|
| **Token Storage**           | Secure storage mechanism | Token expiration       | Seamless re-authentication |
| **Input Sanitization**      | Client-side validation   | Server-side validation | Prevents XSS attacks       |
| **HTTPS Enforcement**       | Redirect HTTP to HTTPS   | SSL certificate        | Secure data transmission   |
| **Content Security Policy** | CSP headers              | API CORS configuration | Protection against attacks |

---

## Integration Timeline

### 14. Frontend Development Phases

| Phase       | Frontend Focus        | API Dependencies | User Testing                |
|-------------|-----------------------|------------------|-----------------------------|
| **Phase 1** | Authentication UI     | Auth endpoints   | Login/registration flow     |
| **Phase 2** | Session management    | Session CRUD     | Session creation/navigation |
| **Phase 3** | Document upload       | Upload endpoints | File upload experience      |
| **Phase 4** | Chat interface        | Chat endpoints   | Conversation flow           |
| **Phase 5** | Dashboard & analytics | Usage endpoints  | Usage tracking UX           |
| **Phase 6** | Polish & optimization | All endpoints    | End-to-end user testing     |

---

## Performance Metrics & Monitoring

### 15. Frontend Performance Targets

| Metric                    | Target                        | Measurement             | User Impact           |
|---------------------------|-------------------------------|-------------------------|-----------------------|
| **Initial Load Time**     | <3 seconds                    | Lighthouse              | First impression      |
| **Chat Response Display** | <100ms after API response     | User interaction timing | Conversation fluidity |
| **File Upload Feedback**  | Immediate progress indication | Upload event handling   | User confidence       |
| **Dashboard Load**        | <2 seconds                    | Page load timing        | User engagement       |
