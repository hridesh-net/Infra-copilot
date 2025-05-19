from sentence_transformers import SentenceTransformer
from backend.docs_engine.weaviate_client import get_weaviate_client
from backend.schemas.context import DocChunk


model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_relevant_chunks(query: str, top_k: int = 3) -> list[DocChunk]:
    """
    Uses semantic vector search to retrieve top-k relevant documentation chunks.
    """
    client = get_weaviate_client()
    query_vector = model.encode(query).tolist()

    results = client.query \
        .get("AWSDoc", ["content", "source"]) \
        .with_near_vector({
            "vector": query_vector,
            "certainty": 0.7
        }) \
        .with_limit(top_k) \
        .do()

    docs = results.get("data", {}).get("Get", {}).get("AWSDoc", [])

    return [
        DocChunk(
            content=item["content"],
            source=item.get("source"),
            score=None,  # You can extract score if returned
            metadata=None
        )
        for item in docs
    ]
