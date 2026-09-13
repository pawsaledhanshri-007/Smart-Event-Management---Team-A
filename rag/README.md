# Smart Event Management - RAG Module

## Overview

This module implements the Retrieval-Augmented Generation (RAG) component for the Smart Event Management System.

The system answers user questions about event information by:

1. Loading event data
2. Splitting the data into chunks
3. Converting chunks into embeddings using SentenceTransformer
4. Storing embeddings in a FAISS vector store
5. Retrieving event information
6. Sending the retrieved information to Gemini
7. Returning a concise answer

## RAG Pipeline

User Question
↓
SentenceTransformer
↓
Question Embedding
↓
FAISS Vector Search
↓
Retrieved Event Information
↓
Gemini
↓
Generated Answer

## Technologies Used

* Python
* Sentence Transformers
* all-MiniLM-L6-v2
* FAISS
* Google Gemini API
* FastAPI
* Uvicorn
* Pydantic

## Current Dataset

The current prototype uses:

`event_data.txt`

The sample event is:

**TechFest 2026**

The event information includes:

* Event name
* Venue
* Event date
* Registration details
* Schedule
* Important information

## Embeddings

Model:

`all-MiniLM-L6-v2`

Embedding dimension:

`384`

Current number of chunks:

`7`

Current FAISS vector count:

`7`

## Running the RAG Application

From the project root:

```powershell
python rag\rag_app.py
```

The program asks:

```text
Enter your question:
```

Example:

```text
Where is the event?
```

Example response:

```text
The event will take place at the Main Auditorium, Kalpataru Institute of Technology.
```

## Running the RAG API

Start the FastAPI server:

```powershell
python -m uvicorn rag.rag_api:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### GET /health

Checks whether the RAG service is running.

Example response:

```json
{
  "status": "RAG service is running"
}
```

### POST /ask

Accepts a user question and returns the generated answer.

Request:

```json
{
  "question": "When is the project exhibition?"
}
```

Response:

```json
{
  "question": "When is the project exhibition?",
  "answer": "The Project Exhibition is scheduled for 02:00 PM on September 20, 2026."
}
```

## Tested Questions

### 1. Where is the event?

**Answer:**

The event will take place at the Main Auditorium, Kalpataru Institute of Technology.

### 2. When is the project exhibition?

**Answer:**

The Project Exhibition is scheduled for 02:00 PM on September 20, 2026.

### 3. When is the registration deadline?

**Answer:**

Participants must register online before September 15, 2026.

### 4. What should participants bring?

**Answer:**

Participants should carry their college ID cards.

## Error Handling

The API includes error handling for temporary RAG or Gemini service failures.

When an exception occurs while processing a question, the API returns HTTP `503` with:

```json
{
  "detail": "The RAG service is temporarily unavailable. Please try again later."
}
```

## Current Status

* RAG pipeline: Completed
* Embedding generation: Completed
* FAISS vector store: Completed
* Gemini answer generation: Completed
* FastAPI API: Completed
* Swagger API testing: Completed
* Health check endpoint: Completed
* Error handling: Implemented
* Documentation: Completed

## Backup Files

Working backups created during development:

* `rag_backup_working.zip`
* `rag_backup_final.zip`
* `rag_api_working_backup.zip`
* `rag_project_final.zip`
* `rag_integration_ready_backup.zip`

## Future Integration

The RAG API is designed to be integrated with the Smart Event Management backend.

Expected integration flow:

Frontend / Agent
↓
Backend
↓
RAG API `/ask`
↓
Retrieval + Gemini
↓
Answer
