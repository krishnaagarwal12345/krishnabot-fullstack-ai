# KrishnaBot — Full Stack AI Application 🤖

## Overview
A complete full stack AI application combining
Python FastAPI + Spring Boot + HTML frontend.

## Architecture
HTML Frontend (port 8080/static)
↓ fetch() HTTP
Spring Boot (port 8080)
↓ WebClient HTTP
Python FastAPI (port 8000)
↓ Groq API
Llama 3.3 70B AI Model

## Features
✅ Normal Chat — general AI conversation
✅ RAG Document Search — answers from documents
✅ FAISS vector search — semantic similarity
✅ Sentence transformer embeddings
✅ Streaming-ready architecture
✅ Professional UI with typing indicator
✅ Source chunks displayed for transparency
✅ Error handling at all layers

## Tech Stack

### Frontend
- HTML5, CSS3, JavaScript (fetch API)

### Backend (Java)
- Spring Boot 3.x
- WebClient (reactive HTTP client)
- Maven

### AI Backend (Python)
- FastAPI
- Groq API (Llama 3.3 70B)
- Sentence Transformers
- FAISS vector database
- Uvicorn

## How to Run

### Step 1 — Start Python AI Backend
```bash
cd python-backend
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

### Step 2 — Start Spring Boot
```bash
cd spring-boot-client
.\mvnw spring-boot:run
```

### Step 3 — Open browser
http://localhost:8080

## API Endpoints

### Python FastAPI (port 8000)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home |
| GET | /health | Health check |
| POST | /api/chat | Normal AI chat |
| POST | /api/rag | RAG document search |
| GET | /api/chunks | View knowledge base |

### Spring Boot (port 8080)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| POST | /api/chat | Forward to Python chat |
| POST | /api/rag | Forward to Python RAG |

## Created By
Krishna — Final Year CS Student
AI/ML Developer | Java + Python + GenAI
