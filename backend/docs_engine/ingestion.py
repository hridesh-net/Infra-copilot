import asyncio

from urllib.parse import urlparse

from src.backend.docs_engine.crawler import Crawler
from src.backend.docs_engine.chunker import chunk_text
from src.backend.docs_engine.embedder import embed_chunks
from src.backend.docs_engine.weaviate_client import WeaviateClient


class Ingestion:

    @classmethod
    async def ingest_docs(cls, topic:str, urls: list[str]):
        """
        Executes the loader to fetch documentation content.
        """

        results = await asyncio.gather(*[Crawler.crawl_url(u) for u in urls], return_exceptions=True)

        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                continue

            text = result

            parsed = urlparse(url)
            service = parsed.path.split("/")[1]

            chunks = chunk_text(
                text,
                metadata={
                    "topic": topic,
                    "url": url,
                    "service": service
                }
            )

            print(f"chunks type: {type(chunks)}")

            vectors = embed_chunks(chunks)

            WeaviateClient.upload_chunks(vectors, topic)
