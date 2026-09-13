print("Answer generation stage started!")

import faiss
from sentence_transformers import SentenceTransformer

# Read the event knowledge file
with open("rag/event_data.txt", "r", encoding="utf-8") as file:
    event_info = file.read()

# Split into chunks
chunks = event_info.split("\n\n")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(chunks)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# User question
question = "When is the project exhibition?"

# Convert question into an embedding
question_embedding = model.encode([question])

# Retrieve the most relevant chunk
distance, result = index.search(question_embedding, k=1)
retrieved_chunk = chunks[result[0][0]]

# Generate a simple answer
if "Project Exhibition" in retrieved_chunk:
    answer = "The project exhibition is scheduled for 02:00 PM."
else:
    answer = "The relevant information was retrieved, but a specific answer could not be generated."

print("\nQuestion:")
print(question)

print("\nRetrieved Information:")
print(retrieved_chunk)

print("\nAnswer:")
print(answer)

print("\nAnswer generation completed successfully!")