import asyncio
from urllib.parse import urlparse
from rag_agent.crawler import crawl_url
from rag_agent.chunker import chunk_text
from rag_agent.embedder import embed_chunks
from rag_agent.weaviate_client import upload_chunks
from rag_agent.logging_config import get_logger

logger = get_logger(__name__)

async def ingest_docs(topic: str, urls: list[str]):
    """
    Orchestrates ingestion pipeline:
      1. Crawl URLs to extract plain text
      2. Chunk text into overlapping segments
      3. Embed chunks into vectors
      4. Upload vectors with metadata to Weaviate
    """
    # Crawl all URLs in parallel
    print(f"doc manager started for {topic} and URL: {urls}")
    results = await asyncio.gather(*[crawl_url(u) for u in urls], return_exceptions=True)

    for url, result in zip(urls, results):
        if isinstance(result, Exception):
            logger.error(f"Failed to crawl {url}: {result}")
            continue
        text = result
        # Derive the service name from the URL path (e.g. 'AmazonECS')
        parsed = urlparse(url)
        # The service is the first path segment after the leading '/'
        service = parsed.path.split("/")[1]
        # Break into chunks with metadata
        chunks = chunk_text(
            text,
            metadata={
                "topic": topic,
                "url": url,
                "service": service
            }
        )
        logger.info(f"Generated {len(chunks)} chunks for {url}")

        # Embed all chunks
        vectors = embed_chunks(chunks)
        logger.info(f"Embedded {len(vectors)} vectors for {url}")

        # Upload to Weaviate
        upload_chunks(vectors, topic)
        logger.info(f"Uploaded vectors for {url}")
