from openai import OpenAI
from rag_agent.config import LLM_MODEL, OPENAI_API_KEY
from rag_agent.retriever import retrieve_chunks

client = OpenAI(api_key=OPENAI_API_KEY)

def build_prompt(chunks: list[dict], query: str) -> str:
    context = "\n\n".join([c["text"] for c in chunks])
    return f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

async def retrieve_and_ask(topic: str, query: str) -> str:
    # 1) Get context chunks
    chunks = retrieve_chunks(topic, query)
    # 2) Build prompt
    prompt = build_prompt(chunks, query)
    # Call LLM using v1 client
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
