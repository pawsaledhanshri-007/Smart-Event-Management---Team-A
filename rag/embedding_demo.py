print("Embedding stage started!")

from sentence_transformers import SentenceTransformer

# Read the event knowledge file
with open("rag/event_data.txt", "r", encoding="utf-8") as file:
    event_info = file.read()

# Split the information into chunks
chunks = event_info.split("\n\n")

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert each chunk into an embedding
embeddings = model.encode(chunks)

print("\nNumber of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

print("\nEmbedding created successfully!")