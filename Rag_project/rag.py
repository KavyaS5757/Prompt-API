import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma = chromadb.PersistentClient(path="./chroma_db")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_collections():
    return [c.name for c in chroma.list_collections()]

def ask(question, collection_name, n_results=4):
    collection = chroma.get_collection(collection_name)

    # embed the question and find similar chunks
    question_embedding = embedder.encode([question]).tolist()
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results
    )

    # build context from top chunks
    chunks = results["documents"][0]
    context = "\n\n---\n\n".join(chunks)

    # send to Groq with context
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that answers questions 
based on the provided document context. 
If the answer isn't in the context, say "I couldn't find that in the document."
Always be concise and cite which part of the document supports your answer."""
            },
            {
                "role": "user",
                "content": f"Context from document:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.2  # low temp for factual accuracy
    )

    return {
        "answer": response.choices[0].message.content,
        "chunks": chunks  # return source chunks too
    }