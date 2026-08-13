import os
import voyageai
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
mongo_client = MongoClient(os.getenv("MONGODB_URI"))

collection = mongo_client["audio_rag"]["transcript_chunks"]

def embed_query(query_text):
    result = voyage_client.contextualized_embed(
        inputs=[[query_text]],
        model="voyage-context-3",
        input_type="query",
    )
    return result.results[0].embeddings[0]

def retrieve(query_text, top_k=3):
    query_embedding = embed_query(query_text)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "autoembed_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 50,
                "limit": top_k,
            }
        },
        {
            "$project": {
                "text": 1,
                "score": {"$meta": "vectorSearchScore"},
                "_id": 0,
            }
        },
    ]

    results = list(collection.aggregate(pipeline))
    return results

if __name__ == "__main__":
    query = "what happens during neural network training"
    results = retrieve(query)
    for r in results:
        print(f"Score: {r['score']:.4f}")
        print(r["text"][:300])
        print("---")