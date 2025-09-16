from openai import OpenAI
from src.backend.docs_engine.config import OPENAI_API_KEY, EMBEDDING_MODEL

op_client = OpenAI(api_key=OPENAI_API_KEY)

def embed_chunks(
    chunks: list[dict],
    batch_size: int = 50
) -> list[dict]:
    embeddings: list[dict] = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        resp = op_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[c["text"] for c in batch],
        )
        for c, item in zip(batch, resp.data):
            embeddings.append({
                "vector": item.embedding,
                "text": c["text"],
                "metadata": c["metadata"],
            })

    return embeddings
