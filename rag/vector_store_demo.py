print("Vector store stage started!")

import faiss
from sentence_transformers import SentenceTransformer

# Read the event knowledge file
with open("rag/event_data.txt", "r", encoding="utf-8") as file:
    event_info = file.read()

# Split the information into chunks
chunks = event_info.split("\n\n")

# Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

# Create a FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Store the embeddings in FAISS
index.add(embeddings)

print("\nNumber of chunks:", len(chunks))
print("Vector dimension:", dimension)
print("Vectors stored in FAISS:", index.ntotal)

print("\nVector store created successfully!")