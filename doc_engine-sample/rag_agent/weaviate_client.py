import os

import weaviate
import weaviate.classes.config as wc
from urllib.parse import urlparse

# from .config import WEAVIATE_URL, WEAVIATE_API_KEY
# from weaviate.warnings import PydanticDeprecatedSince211

# warnings.filterwarnings("ignore", category=PydanticDeprecatedSince211)

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")

parsed = urlparse(WEAVIATE_URL)
host = parsed.hostname or "localhost"
port = parsed.port or 8080

headers = {"X-API-KEY": WEAVIATE_API_KEY} if WEAVIATE_API_KEY else None

client = weaviate.connect_to_local(
    host=host, port=port, grpc_port=50051, headers=headers, skip_init_checks=True
)

CLASS_NAME = "DocumentChunk"


def ensure_schema():
    existing = client.collections.list_all()
    if CLASS_NAME not in existing:
        client.collections.create(
            name=CLASS_NAME,
            properties=[
                wc.Property(name="text",       data_type=wc.DataType.TEXT),
                wc.Property(name="service",    data_type=wc.DataType.TEXT),
                wc.Property(name="topic",      data_type=wc.DataType.TEXT),
                wc.Property(name="url",        data_type=wc.DataType.TEXT),
                wc.Property(name="chunk_id",   data_type=wc.DataType.INT),
                wc.Property(name="start_token",data_type=wc.DataType.INT),
                wc.Property(name="end_token",  data_type=wc.DataType.INT),
            ],
            vectorizer_config=wc.Configure.Vectorizer.none(),
            multi_tenancy_config=wc.Configure.multi_tenancy(
                enabled=True, auto_tenant_creation=True
            ),
        )
    else:
        print(f"Collection '{CLASS_NAME}' already exists.")


def upload_chunks(records: list[dict], tenant: str):
    """
    Upload a batch of chunk records under a specific tenant.
    """
    ensure_schema()
    with client.batch.fixed_size(batch_size=100) as batch:
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
                collection=CLASS_NAME,
                tenant=tenant,
                vector=rec["vector"],
            )
