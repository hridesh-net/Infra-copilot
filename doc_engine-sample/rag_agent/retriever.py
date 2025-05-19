from openai import OpenAI
from rag_agent.config import OPENAI_API_KEY, EMBEDDING_MODEL, TOP_K
from rag_agent.weaviate_client import client as weaviate_client, CLASS_NAME
from weaviate.classes.query import MetadataQuery

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def retrieve_chunks(
    topic: str,
    query: str,
    top_k: int = TOP_K
) -> list[dict]:
    # 1) Embed the query
    resp = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query],
    )
    q_emb = resp.data[0].embedding

    # 2) Vector search filtered by topic using v4 Collections API
    collection = weaviate_client.collections.get(CLASS_NAME)

    tenant_collection = collection.with_tenant(topic)
    query_result = tenant_collection.query.near_vector(
        near_vector=q_emb,
        certainty=0.7,
        limit=top_k,
        return_metadata=MetadataQuery(distance=True)
    )

    # Extract and return the chunk properties
    chunks = [obj.properties for obj in query_result.objects]
    return chunks
