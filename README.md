# AI-Powered Document Chatbot API

> Short tagline / one-liner about the project.

---

## Quick Links
- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)

---

## About

<!-- High-level description of the project, why it exists, who it’s for. -->

The **AI-Powered Document Chatbot** web application built with FastAPI. The 
application allows users to upload documents, ask questions in natural language, 
and receive intelligent answers powered by RAG (Retrieval-Augmented Generation).

---

## Features

<!-- Bullet points of key features (MVP + nice-to-have). -->

- JWT-based authentication
- Chatbot sessions for different use cases
- Document upload with file size & format validation
- Document embedding & vector search (via FAISS)
- Chat history per session
- PDF/text export of entire conversations
- Token usage tracking per user
- RESTful API with FastAPI and async tasks

---

## Architecture

<!-- Brief description of system architecture (can link to ARCHITECTURE.md). -->

**Frontend:** React.js  
**Backend:** FastAPI (Python)  
**Database:** PostgresSQL (users, sessions, metadata)  
**Vector DB:** FAISS 
**Storage:** Local or Cloud (S3, etc.)  
**Auth:** JWT access & refresh tokens (cookie or header)  
**Background Tasks:** Celery / FastAPI tasks  
**LLM API:** OpenAI / Claude / Llama.cpp

---

## Tech Stack

<!-- List backend, database, libraries, tools, cloud services. -->

---

## Project Structure

<!-- Project Structure -->

---

## Database Design

<!-- Brief summary of tables/relationships (link to DATABASE_DESIGN.md). -->

---

## API Documentation

- Interactive docs via Swagger UI: /docs

- Alternative ReDoc: /redoc

- Full API spec: see [API Documentation](./docs/API_ENDPOINTS.md)

---

## Testing

- Unit Tests: services, utils, repositories

- Integration Tests: DB + API endpoints

- End-to-End Tests: chatbot session workflows

---

## Deployment

- Local (Docker Compose)

- Production (e.g. Render, AWS, or GCP)

See [Deployment Plan](./docs/DEPLOYMENT.md) for details.

---

## Roadmap

<!-- Describe feature roadmap -->

---

## Support

**Built with ❤️ by [Emmanuel M-A](https://github.com/EmmanuelM-A)**

***Tears and sweat aren’t the foundation, but they’re the path to one. Happy coding!***


