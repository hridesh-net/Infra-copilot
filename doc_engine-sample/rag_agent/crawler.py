import httpx
from bs4 import BeautifulSoup
import tempfile
import os

from rag_agent.logging_config import get_logger

logger = get_logger(__name__)

async def fetch_html(url: str) -> str:
    """Fetches an HTML page and returns its text content."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url)
        resp.raise_for_status()
    return resp.text

async def fetch_pdf(url: str) -> str:
    """Downloads a PDF and extracts its text."""
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(url)
        resp.raise_for_status()
    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.write(resp.content)
    tmp.close()
    # Extract text via pdfminer or similar
    # TODO: implement PDF parsing
    text = ""  # placeholder
    os.unlink(tmp.name)
    return text

async def crawl_url(url: str) -> str:
    """Detect content type and fetch accordingly."""
    if url.lower().endswith('.pdf'):
        return await fetch_pdf(url)
    else:
        html = await fetch_html(url)
        # Parse with BeautifulSoup to strip navbars, footers, scripts
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)
