# DEPLOYMENT

This document describes how to deploy the **DocuChatAPI** application across local
development and production environments. It also explains how vector embeddings 
(FAISS index + metadata) will be stored and accessed.

---

## Vector Database Design

The application uses **per-user vector stores** to store document embeddings and metadata.  
This allows multiple chat sessions to share the same knowledge base while keeping user data isolated.

### Approach

- **One vector store per user** (at least for MVP).  
- Chat sessions reference the user’s vector store when retrieving relevant documents.  
- Metadata (document filename, session ID, token usage, etc.) is stored alongside vectors for traceability.  

### Storage Options

1. **Local FAISS + Pickle (MVP)**  
   - Store FAISS index as a binary file (`user_{id}_index.faiss`) in a local or mounted volume.  
   - Store metadata (doc IDs, filenames, embeddings → original doc mapping) as a Pickle or JSON file (`user_{id}_meta.pkl`).  
   - Use a structured directory per user:
     ```
     /vector_store/
       ├── user_<uuid>/
       │   ├── index.faiss
       │   └── metadata.pkl
     ```

2. **External Vector DB (Scalable Upgrade)**  
   - Replace FAISS with a managed vector DB (e.g., **Pinecone**, **Weaviate**, or **Milvus**).  
   - Store vectors under **user namespaces**, metadata in Postgres.  
   - This decouples storage from API instances and makes scaling easier.

---

## Local Development

During development, the deployment strategy is kept simple:

- **Postgres Database**  
  - Run via Docker (`docker-compose.yml`) on localhost.  
  - Used for relational data (users, sessions, chat history, usage stats).  

- **Vector Store**  
  - FAISS indexes + metadata Pickle files stored locally in `./vector_store/`.  
  - Developers can inspect, reset, or reload indexes easily.  

- **Application API**  
  - Run FastAPI locally (`uvicorn src.server:app --reload`).  
  - Auto-reloads with code changes.  

- **Environment Variables** (`.env`)  
  - Store DB connection strings, secret keys, and any AI API keys.  
  - Example:
    ```
    DATABASE_URL=postgresql://user:password@localhost:5432/docuchat
    VECTOR_STORE_PATH=./vector_store
    OPENAI_API_KEY=sk-xxxx
    ```

---

## Production

For production deployment, the application should be **containerized** and run on 
a **cloud environment** with persistent storage and monitoring.

### Recommended Setup

1. **Infrastructure**  
   - **API Layer**: FastAPI app container (Docker).  
   - **Relational DB**: Managed Postgres (AWS RDS, GCP Cloud SQL, etc.).  
   - **Vector Store**:  
     - Option A: Persist FAISS indexes in a mounted network volume (e.g., AWS EFS).  
     - Option B (Preferred at scale): Use an external vector DB (Pinecone, Weaviate, Milvus).  

2. **Orchestration**  
   - Use **Docker Compose** for simple deployment.  
   - For scaling: use **Kubernetes (K8s)** with pods for API, Postgres, and a storage-backed vector DB.  

3. **Deployment Workflow**  
   - CI/CD pipeline (GitHub Actions, GitLab CI, etc.).  
   - Automated builds push Docker images to a container registry.  
   - Deployment scripts (Helm/K8s manifests or Docker Compose for small scale).  

4. **Security**  
   - Environment variables stored in **secrets manager** (AWS Secrets Manager, Vault, etc.).  
   - SSL termination via **NGINX or API Gateway**.  
   - JWT authentication middleware.  

5. **Persistence**  
   - **Postgres**: Use managed or volume-backed DB for durability.  
   - **FAISS/Vector DB**:  
     - If FAISS: mount persistent volumes.  
     - If managed DB: persistence is handled by provider.  

6. **Monitoring & Logging**  
   - Use **Prometheus + Grafana** (if Kubernetes).  
   - Centralized logging via **ELK stack** or cloud-native logging.  

---

### Deployment Summary Table

| Component     | Local Dev                     | Production (MVP)                      | Production (Scale)            |
|---------------|-------------------------------|---------------------------------------|-------------------------------|
| API           | Uvicorn (FastAPI, reload)     | Docker container                      | K8s pods (scalable replicas)  |
| Postgres DB   | Local Docker container        | Managed Postgres (RDS/Cloud SQL)      | Same                          |
| Vector Store  | Local FAISS + Pickle files    | FAISS w/ persistent volume (EFS, NFS) | External Vector DB (Pinecone) |
| Deployment    | Run manually / Docker Compose | Docker Compose or simple VM setup     | CI/CD → K8s + Helm            |
| Env Variables | `.env` file                   | Cloud Secrets Manager                 | Same                          |

---


