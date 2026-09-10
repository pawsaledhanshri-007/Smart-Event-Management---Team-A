from google import genai
from sentence_transformers import SentenceTransformer
import faiss


# -----------------------------
# Gemini client
# -----------------------------
client = genai.Client()


# -----------------------------
# Load event data
# -----------------------------
def load_event_data():
    with open("rag/event_data.txt", "r", encoding="utf-8") as file:
        data = file.read()

    print("Event data loaded successfully!")
    return data


# -----------------------------
# Split event data into chunks
# -----------------------------
def split_event_data(data):
    chunks = [chunk.strip() for chunk in data.split("\n\n") if chunk.strip()]

    print(f"Number of chunks: {len(chunks)}")
    return chunks


# -----------------------------
# Create embeddings
# -----------------------------
def create_embeddings(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(chunks)

    print("\nEmbeddings created successfully!")
    print("Embedding shape:", embeddings.shape)

    return model, embeddings


# -----------------------------
# Create FAISS vector store
# -----------------------------
def create_vector_store(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print("\nVector store created successfully!")
    print("Vectors stored:", index.ntotal)
    print("Vector dimension:", dimension)

    return index


# -----------------------------
# Generate answer using Gemini
# -----------------------------
def generate_answer(question, retrieved_chunk):

    prompt = f"""
You are an AI assistant for a Smart Event Management System.

Answer the user's question using ONLY the information provided below.

Event Information:
{retrieved_chunk}

User Question:
{question}

Give ONLY the answer to the user's question.

Do not repeat the event information.
Do not provide unrelated details.
Do not explain your reasoning.
Keep the answer to 1-2 sentences.

If the answer is not available in the provided information, say:
"I could not find that information in the event data."
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# -----------------------------
# Retrieve relevant information
# -----------------------------
def answer_question(question, model, index, chunks):

    question_embedding = model.encode([question])

    # Current prototype has only 7 chunks,
    # so retrieve all chunks for reliable answers.
    distances, indices = index.search(question_embedding, k=7)

    retrieved_chunks = [chunks[i] for i in indices[0]]

    retrieved_chunk = "\n\n".join(retrieved_chunks)

    answer = generate_answer(question, retrieved_chunk)

    return answer


# -----------------------------
# Main program
# -----------------------------
if __name__ == "__main__":

    data = load_event_data()

    chunks = split_event_data(data)

    model, embeddings = create_embeddings(chunks)

    index = create_vector_store(embeddings)

    question = input("\nEnter your question: ")

    answer = answer_question(
        question,
        model,
        index,
        chunks
    )

    print("\nQuestion:", question)
    print("\nGenerated Answer:")
    print(answer)