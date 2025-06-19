from openai import OpenAI
from src.backend.docs_engine.weaviate_client import WeaviateClient
from src.backend.schemas.context import DocChunk
from src.backend.docs_engine.config import OPENAI_API_KEY, EMBEDDING_MODEL

op_client = OpenAI(api_key=OPENAI_API_KEY)


def retrieve_relevant_chunks(query: str, tenant: str, top_k: int = 3) -> list[DocChunk]:
    """
    Uses semantic vector search to retrieve top-k relevant documentation chunks.
    """

    resp = op_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query],
    )
    query_vector = resp.data[0].embedding

    raw_results = WeaviateClient.search(vector=query_vector, tenant=tenant, top_k=top_k)


    chunks = []
    for item in raw_results:
        score = item.get("_additional", {}).get("certainty")  # optional if available
        chunks.append(DocChunk(
            content=item["text"],
            source=item["url"],
            score=score,
            metadata={
                "service": item.get("service"),
                "topic": item.get("topic"),
                "chunk_id": item.get("chunk_id"),
            }
        ))

    return chunks
