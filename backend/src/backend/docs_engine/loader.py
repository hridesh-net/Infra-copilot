import asyncio

from urllib.parse import urlparse

from backend.docs_engine.crawler import Crawler
from backend.docs_engine.chunker import chunk_text
from backend.docs_engine.embedder import embed_chunks
from backend.docs_engine.loaders.aws_loaders import AWSLoader
from backend.docs_engine.weaviate_client import WeaviateClient
from backend.docs_engine.loaders.base_loader import BaseDocLoader


# Register available loaders here
DOC_LOADERS = {
    "aws_doc": AWSLoader,
    # "terraform_doc": TerraformLoader,  # To be added later
}


class DocLoader:
    """
    Loader dispatcher that wraps a specific documentation loader implementation.
    """

    def __init__(self, loader_class: type[BaseDocLoader]):
        if not issubclass(loader_class, BaseDocLoader):
            raise TypeError("loader_class must be a subclass of BaseDocLoader")
        self.loader: BaseDocLoader = loader_class()

    async def ingest_docs(self, topic:str, urls: list[str]):
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

            vectors = embed_chunks(chunks)

            WeaviateClient.upload_chunks(vectors, chunks)
