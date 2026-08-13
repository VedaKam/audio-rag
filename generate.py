import os
from openai import OpenAI
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_answer(query_text, top_k=3):
    chunks = retrieve(query_text, top_k=top_k)
    context = "\n\n".join([c["text"] for c in chunks])

    prompt = f"""Answer the question using only the context below. If the context doesn't contain the answer, say so.

Context:
{context}

Question: {query_text}

Answer:"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-v3.2",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    query = "what did they say about neural networks"  # match or change from step 3
    answer = generate_answer(query)
    print("Answer:\n", answer)