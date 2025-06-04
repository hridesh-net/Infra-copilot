import os
import weaviate
import weaviate.classes.config as wc

from urllib.parse import urlparse

class WeaviateClient:
    """
    Singleton-style utility class for communicating with Weaviate.
    Supports connection, schema management, embedding uploads, and retrieval.
    """

    CLASS_NAME = "DocumentChunk"
    _client = None

    @classmethod
    def _init_client(cls):
        if cls._client is None:
            url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
            api_key = os.getenv("WEAVIATE_API_KEY", "")

            parsed = urlparse(url)
            host = parsed.hostname or "localhost"
            port = parsed.port or 8080
            headers = {"X-API-KEY": api_key} if api_key else None

            cls._client = weaviate.connect_to_local(
                host=host,
                port=port,
                grpc_port=50051,
                headers=headers,
                skip_init_checks=True
            )

    @classmethod
    def get_client(cls):
        cls._init_client()
        return cls._client

    @classmethod
    def ensure_schema(cls):
        cls._init_client()
        existing = cls._client.collections.list_all()
        if cls.CLASS_NAME not in existing:
            cls._client.collections.create(
                name=cls.CLASS_NAME,
                properties=[
                    wc.Property(name="text", data_type=wc.DataType.TEXT),
                    wc.Property(name="service", data_type=wc.DataType.TEXT),
                    wc.Property(name="topic", data_type=wc.DataType.TEXT),
                    wc.Property(name="url", data_type=wc.DataType.TEXT),
                    wc.Property(name="chunk_id", data_type=wc.DataType.INT),
                    wc.Property(name="start_token", data_type=wc.DataType.INT),
                    wc.Property(name="end_token", data_type=wc.DataType.INT),
                ],
                vectorizer_config=wc.Configure.Vectorizer.none(),
                multi_tenancy_config=wc.Configure.multi_tenancy(
                    enabled=True, auto_tenant_creation=True
                ),
            )

    @classmethod
    def upload_chunks(cls, records: list[dict], tenant: str):
        """
        Uploads a batch of vectorized document chunks.
        """
        cls.ensure_schema()
        with cls._client.batch.fixed_size(batch_size=100) as batch:
            for rec in records:
                props = {
                    "text": rec["text"],
                    "service": rec["metadata"]["service"],
                    "topic": rec["metadata"]["topic"],
                    "url": rec["metadata"]["url"],
                    "chunk_id": rec["metadata"]["chunk_id"],
                    "start_token": rec["metadata"]["start_token"],
                    "end_token": rec["metadata"]["end_token"],
                }
                batch.add_object(
                    properties=props,
                    collection=cls.CLASS_NAME,
                    tenant=tenant,
                    vector=rec["vector"]
                )

    @classmethod
    def search(cls, vector: list[float], tenant: str, top_k: int = 3) -> list[dict]:
        """
        Search the collection using a vector query.
        """
        cls._init_client()
        results = cls._client.query \
            .get(cls.CLASS_NAME, ["text", "url", "service", "topic", "chunk_id"]) \
            .with_tenant(tenant) \
            .with_near_vector({"vector": vector, "certainty": 0.7}) \
            .with_limit(top_k) \
            .do()

        return results.get("data", {}).get("Get", {}).get(cls.CLASS_NAME, [])
