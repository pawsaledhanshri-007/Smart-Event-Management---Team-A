from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
from google import genai
client = genai.Client()

def load_event_data():
    file_path = Path(__file__).parent / "event_data.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    return data


def split_event_data(data):
    chunks = data.split("\n\n")
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks



def generate_answer(question, retrieved_chunk):
    prompt = f"""
You are an AI assistant for a Smart Event Management System.

Answer the user's question using ONLY the information provided below.

Event Information:
{retrieved_chunk}

User Question:
{question}

Give a clear and concise answer.
If the information is not available in the event information, say:
"I could not find that information in the event data."
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text




def answer_question(question):
    question_embedding = model.encode([question])

    distances, indices = index.search(question_embedding, k=3)

    retrieved_chunks = [chunks[i] for i in indices[0]]

    retrieved_chunk = "\n\n".join(retrieved_chunks)

    answer = generate_answer(question, retrieved_chunk)

    return answer




# Load event data
event_data = load_event_data()

# Split data into chunks
chunks = split_event_data(event_data)

print("Event data loaded successfully!")
print("Number of chunks:", len(chunks))


# Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

print("\nEmbeddings created successfully!")
print("Embedding shape:", embeddings.shape)


# Create vector store
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("\nVector store created successfully!")
print("Vectors stored:", index.ntotal)
print("Vector dimension:", dimension)


# Ask a question
# Ask a question
question = input("\nEnter your question: ")

answer = answer_question(question)

print("\nQuestion:", question)
print("\nGenerated Answer:")
print(answer)