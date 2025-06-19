import os
from uuid import uuid4
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue


class QdrantDB:

    """
    Singleton-style client to interact with Qdrant for:
    - Initializing collections
    - Uploading embedded chunks
    - Searching for relevant documentation

    Supports multiple cloud platforms: AWS, GCP, Azure, Terraform.
    """

    _client: QdrantClient = None
    _default_url = os.getenv("QDRANT_URL", "http://localhost:6333")

    @classmethod
    def get_client(cls) -> QdrantClient:
        if cls._client is None:
            cls._client = QdrantClient(url=cls._default_url)
        return cls._client

    @classmethod
    def ensure_collection(cls, collection: str, vector_size: int = 384):
        """
        Creates collection if not already present.
        """
        client = cls.get_client()
        collections = client.get_collections().collections
        if not any(c.name == collection for c in collections):
            client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )


    @classmethod
    def upload_chunks(
        cls,
        collection: str,
        docs: list[dict[str, Any]],
        vectors: list[list[float]]
    ):
        """
        Uploads embedded chunks to the given collection.

        Each doc should contain:
            - text: str
            - metadata: dict (service, topic, provider, url, etc.)
        """
        cls.ensure_collection(collection, vector_size=len(vectors[0]))

        points = []

        for doc, vec in zip(docs, vectors):
            payload = {
                "text": doc["text"],
                **doc.get("metadata", {})
            }
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=vec,
                    payload=payload
                )
            )

        cls.get_client().upsert(collection_name=collection, points=points)


    @classmethod
    def search(
        cls,
        collection: str,
        query_vector: list[float],
        top_k: int = 5,
        provider_filter: str = None
    ) -> list[dict[str, Any]]:
        """
        Performs semantic search in the given collection.

        Optionally filter by cloud provider (aws, gcp, azure, terraform).
        """

        cls.ensure_collection(collection, vector_size=len(query_vector))

        search_filter = None
        if provider_filter:
            search_filter = Filter(
                must=[FieldCondition(key="provider", match=MatchValue(value=provider_filter))]
            )

        results = cls.get_client().search(
            collection_name=collection,
            query_vector=query_vector,
            limit=top_k,
            query_filter=search_filter
        )

        return [hit.pauload for hit in results]
