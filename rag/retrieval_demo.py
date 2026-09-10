print("Retrieval stage started!")

import faiss
from sentence_transformers import SentenceTransformer

# Read the event knowledge file
with open("rag/event_data.txt", "r", encoding="utf-8") as file:
    event_info = file.read()

# Split the information into chunks
chunks = event_info.split("\n\n")

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for the chunks
embeddings = model.encode(chunks)

# Create FAISS vector store
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# User's question
question = "When is the project exhibition?"

# Convert the question into an embedding
question_embedding = model.encode([question])

# Search for the most relevant chunk
distance, result = index.search(question_embedding, k=1)

# Get the retrieved chunk
retrieved_chunk = chunks[result[0][0]]

print("\nQuestion:")
print(question)

print("\nRetrieved Information:")
print(retrieved_chunk)

print("\nRetrieval completed successfully!")