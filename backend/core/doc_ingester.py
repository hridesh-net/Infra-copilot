# doc_ingestor.py
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from qdrant_service import QdrantDB


class DocIngestor:
    """
    Given a documentation URL and provider (aws, azure, gcp, terraform),
    this class scrapes content, chunks it, embeds it, and stores in Qdrant.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def load_html(self, url: str) -> str:
        """
        Scrapes and returns all paragraph content from a documentation URL.
        """
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text() for p in paragraphs)

    def chunk_text(self, text: str, chunk_size: int = 300) -> list[str]:
        """
        Splits text into paragraph-level chunks.
        """
        paragraphs = text.split("\n")
        chunks, current = [], ""
        for para in paragraphs:
            if len(current + para) < chunk_size:
                current += para + "\n"
            else:
                chunks.append(current.strip())
                current = para
        chunks.append(current.strip())
        return chunks

    def infer_topic(self, url: str) -> str:
        """
        Infers the topic or service from the URL (e.g. 's3', 'ec2').
        """
        return url.split("/")[-1].lower().split(".")[0]  # crude but works for most docs

    def ingest(self, url: str, provider: str, collection: str = "cloud_docs"):
        """
        Main entry point to ingest docs from a URL and store in Qdrant.
        """
        text = self.load_html(url)
        chunks = self.chunk_text(text)
        embeddings = self.model.encode(chunks).tolist()
        topic = self.infer_topic(url)

        records = []
        for i, chunk in enumerate(chunks):
            records.append({
                "text": chunk,
                "metadata": {
                    "provider": provider,
                    "service": topic,
                    "topic": topic,
                    "url": url,
                    "chunk_id": i,
                    "start_token": 0,
                    "end_token": len(chunk.split())
                }
            })

        QdrantDB.upload_chunks(collection=collection, docs=records, vectors=embeddings)


if __name__ == "__main__":
    ingestor = DocIngestor()

    ingestor.ingest(
        url="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html",
        provider="aws"
    )
