import requests
from bs4 import BeautifulSoup
from backend.src.backend.docs_engine.loaders.base_loader import BaseDocLoader

class AWSLoader(BaseDocLoader):

    async def load(self, url: str) -> str:
        """
        Fetches and extracts text from an AWS documentation page.
        """
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        content = "\n".join([p.text for p in soup.find_all("p")])
        return content
