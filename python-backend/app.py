from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import time
import os

# ============================================
# CONFIGURATION
# ============================================
GROQ_API_KEY =os.environ.get("GROQ_API_KEY", "")
MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ============================================
# INITIALIZE
# ============================================
print("Starting KrishnaBot AI API...")
embed_model = SentenceTransformer(EMBEDDING_MODEL)
groq_client = Groq(api_key=GROQ_API_KEY)
print("Models loaded! ✅")

# ============================================
# FASTAPI APP
# ============================================
app = FastAPI(
    title="KrishnaBot AI API",
    description="Full Stack AI API — RAG + Chat powered by Llama AI",
    version="1.0.0"
)

# CORS — allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# KNOWLEDGE BASE
# ============================================
KNOWLEDGE_BASE = """
The company offers 20 days of annual leave per year.
Office hours are 9 AM to 6 PM Monday to Friday.
Employees can work from home on Wednesdays and Fridays.
Performance reviews happen every 6 months.
Salary increments happen every April.
Average increment is 15 percent for good performers.
Exceptional performers get 25 percent increment.
Health insurance covers entire family including parents.
New employees get laptop and equipment on day one.
Buddy program pairs new employees with senior members.
The company was founded in 2010 with 500 employees.
Office is located in Bangalore on MG Road.
Free lunch is provided in office cafeteria.
Bonuses are given every December.
Maternity leave is 26 weeks as per company policy.
"""

# ============================================
# BUILD RAG INDEX ON STARTUP
# ============================================
print("Building RAG index...")
chunks = [s.strip() for s in
          KNOWLEDGE_BASE.split('\n') if s.strip()]
embeddings = embed_model.encode(chunks)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))
print(f"RAG index ready with {len(chunks)} chunks! ✅")

# ============================================
# REQUEST / RESPONSE MODELS
# ============================================
class ChatRequest(BaseModel):
    message: str = ""
    question: str = ""
    system_prompt: str = "You are a helpful AI assistant."

class ChatResponse(BaseModel):
    response: str
    model: str
    chunks: list
    time_taken: float

# ============================================
# HELPER FUNCTIONS
# ============================================
def search_chunks(query: str, k: int = 3):
    """Find most relevant chunks for a query"""
    query_embed = embed_model.encode([query])
    distances, indices = index.search(
        np.array(query_embed), k
    )
    return [chunks[indices[0][i]] for i in range(k)]

def call_llm(prompt: str, system: str = None):
    """Call Llama AI via Groq"""
    messages = []
    if system:
        messages.append({
            "role": "system",
            "content": system
        })
    messages.append({
        "role": "user",
        "content": prompt
    })

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

# ============================================
# ENDPOINTS
# ============================================
@app.get("/")
def home():
    return {
        "message": "KrishnaBot AI API Running! 🤖",
        "version": "1.0.0",
        "endpoints": [
            "GET  /health",
            "POST /api/chat",
            "POST /api/rag",
            "GET  /api/chunks"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "model": MODEL,
        "chunks_loaded": len(chunks)
    }

@app.post("/api/chat", response_model=ChatResponse)
def normal_chat(request: ChatRequest):
    """Normal AI chat endpoint"""
    start = time.time()

    user_message = request.message or request.question
    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    try:
        response = call_llm(
            user_message,
            request.system_prompt
        )
        return ChatResponse(
            response=response,
            model=MODEL,
            chunks=[],
            time_taken=round(time.time() - start, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag", response_model=ChatResponse)
def rag_chat(request: ChatRequest):
    """RAG chat endpoint — answers from documents"""
    start = time.time()

    user_query = request.question or request.message
    if not user_query:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        # Search relevant chunks
        relevant = search_chunks(user_query)
        context = "\n".join([
            f"- {chunk}" for chunk in relevant
        ])

        # Build RAG prompt
        prompt = f"""Answer using ONLY the context below.
If answer not in context — say "I don't have that information."

Context:
{context}

Question: {user_query}

Answer:"""

        response = call_llm(prompt,request.system_prompt)

        return ChatResponse(
            response=response,
            model=MODEL,
            chunks=relevant,
            time_taken=round(time.time() - start, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chunks")
def get_chunks():
    """See all knowledge base chunks"""
    return {
        "total": len(chunks),
        "chunks": chunks
    }