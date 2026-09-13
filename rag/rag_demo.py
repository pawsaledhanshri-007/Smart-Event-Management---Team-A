print("RAG setup started successfully!")

# Read information from our event knowledge file
with open("rag/event_data.txt", "r", encoding="utf-8") as file:
    event_info = file.read()

# Split the event information into smaller chunks
chunks = event_info.split("\n\n")

print("\nNumber of chunks:", len(chunks))

print("\n--- Chunks ---")
for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}:")
    print(chunk)