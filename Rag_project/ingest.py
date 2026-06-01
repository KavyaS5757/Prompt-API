import fitz  # pymupdf
import chromadb
from sentence_transformers import SentenceTransformer
import os

embedder = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, free
client = chromadb.PersistentClient(path="./chroma_db")

def load_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest_pdf(filepath):
    filename = os.path.basename(filepath)
    collection_name = filename.replace(".pdf", "").replace(" ", "_")[:50]

    # delete old version if exists
    try:
        client.delete_collection(collection_name)
    except:
        pass

    collection = client.create_collection(collection_name)

    print(f"Reading {filename}...")
    text = load_pdf(filepath)

    print("Splitting into chunks...")
    chunks = chunk_text(text)

    print(f"Embedding {len(chunks)} chunks...")
    embeddings = embedder.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(f"Done! {len(chunks)} chunks stored.")
    return collection_name, len(chunks)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ingest.py uploads/yourfile.pdf")
    else:
        ingest_pdf(sys.argv[1])