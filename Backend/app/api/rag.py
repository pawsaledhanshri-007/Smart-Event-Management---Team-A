from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rag.rag_app import (
    load_event_data,
    split_event_data,
    create_embeddings,
    create_vector_store,
    generate_answer,
)

router = APIRouter()


data = load_event_data()
chunks = split_event_data(data)

model, embeddings = create_embeddings(chunks)
index = create_vector_store(embeddings)


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
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

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="The RAG service is temporarily unavailable."
        )


@router.get("/health")
def health_check():
    return {
        "status": "RAG service is running"
    }