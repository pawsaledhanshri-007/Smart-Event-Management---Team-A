from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .rag_app import (
    load_event_data,
    split_event_data,
    create_embeddings,
    create_vector_store,
    generate_answer
)


# --------------------------------
# Load RAG components once
# --------------------------------

data = load_event_data()
chunks = split_event_data(data)

model, embeddings = create_embeddings(chunks)
index = create_vector_store(embeddings)


# --------------------------------
# FastAPI application
# --------------------------------

app = FastAPI(
    title="Smart Event Management RAG API",
    description="API for answering event-related questions using RAG",
    version="1.0.0"
)


# --------------------------------
# Request model
# --------------------------------

class QuestionRequest(BaseModel):
    question: str


# --------------------------------
# API endpoint
# --------------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:
        question_embedding = model.encode([request.question])

        distances, indices = index.search(
            question_embedding,
            k=7
        )

        retrieved_chunks = [chunks[i] for i in indices[0]]

        retrieved_chunk = "\n\n".join(retrieved_chunks)

        answer = generate_answer(
            request.question,
            retrieved_chunk
        )

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="The RAG service is temporarily unavailable. Please try again later."
        )


# --------------------------------
# Health check endpoint
# --------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "RAG service is running"
    }