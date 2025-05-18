from sentence_transformers import SentenceTransformer
from backend.docs_engine.weaviate_client import get_weaviate_client

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_and_store(chunks: list[str], source_url: str):
    """
    Embeds each chunk and stores it in Weaviate.
    """
    client = get_weaviate_client()
    for chunk in chunks:
        vec = model.encode(chunk).tolist()
        client.data_object.create(
            data_object={"content": chunk, "source": source_url},
            class_name="AWSDoc",
            vector=vec
        )
