import os
import voyageai
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
mongo_client = MongoClient(os.getenv("MONGODB_URI"))

db = mongo_client["audio_rag"]
collection = db["transcript_chunks"]

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def embed_and_store(transcript_path):
    with open(transcript_path, "r") as f:
        text = f.read()

    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks")

    # voyage-context-3 takes a list of chunks and embeds them with full-document context
    result = voyage_client.contextualized_embed(
        inputs=[chunks], 
        model="voyage-context-3",
        input_type="document",
    )

    embeddings = result.results[0].embeddings

    docs = []
    for chunk, embedding in zip(chunks, embeddings):
        docs.append({
            "text": chunk,
            "embedding": embedding,
        })

    collection.delete_many({}) 
    collection.insert_many(docs)
    print(f"Inserted {len(docs)} chunks into MongoDB")

if __name__ == "__main__":
    embed_and_store("transcript.txt")