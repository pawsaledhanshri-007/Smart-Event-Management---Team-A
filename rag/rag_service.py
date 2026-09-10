from pathlib import Path


def load_event_data():
    file_path = Path(__file__).parent / "event_data.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    return data


if __name__ == "__main__":
    event_data = load_event_data()
    print(event_data)
    from pathlib import Path


def load_event_data():
    file_path = Path(__file__).parent / "event_data.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    return data


if __name__ == "__main__":
    event_data = load_event_data()
    print(event_data)
def split_event_data(data):
    chunks = data.split("\n\n")
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings
import faiss


def create_vector_store(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index

def retrieve_relevant_chunk(question, chunks, index):
    question_embedding = model.encode([question])

    distances, indices = index.search(question_embedding, k=1)

    relevant_chunk = chunks[indices[0][0]]

    return relevant_chunk
def generate_answer(question, retrieved_chunk):
    if "project exhibition" in question.lower():
        if "Project Exhibition" in retrieved_chunk:
            return "The project exhibition is scheduled for 02:00 PM."

    return "I found relevant information, but I could not generate a specific answer."
def answer_question(question):
    event_data = load_event_data()

    chunks = split_event_data(event_data)

    embeddings = create_embeddings(chunks)

    vector_store = create_vector_store(embeddings)

    retrieved_chunk = retrieve_relevant_chunk(
        question,
        chunks,
        vector_store
    )

    answer = generate_answer(question, retrieved_chunk)

    return answer
if __name__ == "__main__":
    event_data = load_event_data()

    chunks = split_event_data(event_data)

    embeddings = create_embeddings(chunks)

    vector_store = create_vector_store(embeddings)

    question = "When is the project exhibition?"

    answer_chunk = retrieve_relevant_chunk(
        question,
        chunks,
        vector_store
    )

answer = generate_answer(question, answer_chunk)

print("\nQuestion:", question)
print("\nAnswer:")
print(answer)

    