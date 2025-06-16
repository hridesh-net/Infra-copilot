import os
import httpx
import tempfile

from bs4 import BeautifulSoup

class Crawler:

    @classmethod
    async def fetch_html(cls, url: str) -> str:
        """Fetches an HTML page and return it's text content.

        Args:
            url (str): url needs to be crawled over or from which content should be fetched

        Returns:
            str: Text content from the HTML page
        """
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url)
            resp.raise_for_status()

        return resp.text

    @classmethod
    async def fetch_pdf(cls, url: str) -> str:
        """Downloads PDF and extracts its texts

        Args:
            url (str): url which needs to be extracted

        Returns:
            str: returns extracted pdf content as string
        """
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.get(url)
            resp.raise_for_status()

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.write(resp.content)
        tmp.close()

        # TODO: Implement PDF Parsing

        text = ""
        os.unlink(tmp.name)
        return text

    @classmethod
    async def crawl_url(cls, url: str) -> str:
        """Detect content type and fetch accordingly.

        Args:
            url (str): url needs to be extracted

        Returns:
            str: return parsed meaning full content
        """
        if url.lower().endswith('.pdf'):
            return await cls.fetch_pdf(url)
        else:
            html = await cls.fetch_html(url)

            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()

            return soup.get_text(separator=' ', strip=True)
