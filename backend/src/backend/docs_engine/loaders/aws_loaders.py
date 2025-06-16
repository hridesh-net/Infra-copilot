import requests
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

from src.backend.docs_engine.ingestion import Ingestion
from src.backend.docs_engine.loaders.base_loader import BaseDocLoader

AWS_SITEMAP_INDEX = "https://docs.aws.amazon.com/sitemap_index.xml"


class AWSLoader(BaseDocLoader):

    def __init__(self, max_guides=10, logger=None):
        self.collected: list[str] = []
        self.MAX_GUIDES = max_guides
        self.logger = logger

    def _fetch_sitemap(self, sitemap_url=AWS_SITEMAP_INDEX) -> list[str]:
        """
        Download and parse a sitemap or sitemap-index, returning all <loc> URLs.
        Recurses if this is a sitemapindex.
        Handles non-XML and parse errors gracefully.
        """

        self.logger.info("Sitemap fetching Process Started")

        if len(self.collected) >= self.MAX_GUIDES:
            return self.collected

        try:
            resp = requests.get(sitemap_url, timeout=30)
            resp.raise_for_status()
            content_type = resp.headers.get("Content-Type", "")

            if "xml" not in content_type:
                if any(
                    seg in sitemap_url
                    for seg in [
                        "/latest/userguide/",
                        "/latest/developerguide/",
                        "/latest/APIReference/",
                        "/latest/bestpracticesguide/",
                    ]
                ):
                    if len(self.collected) < self.MAX_GUIDES:
                        self.collected.append(sitemap_url)
                    return self.collected
                return self.collected
            try:
                root = ET.fromstring(resp.text)
            except ET.ParseError as e:
                self.logger.exception(f"Caught err: {e}")
                return self.collected

            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [elem.text for elem in root.findall(".//sm:loc", ns)]

            if root.tag.lower().endswith("sitemapindex"):
                for sub in locs:
                    if len(self.collected) >= self.MAX_GUIDES:
                        break
                    try:
                        self._fetch_sitemap(sub)
                    except Exception as sub_exc:
                        self.logger.exception(f"Error fetching sub-sitemap {sub}: {sub_exc}")
                        print(f"Error fetching sub-sitemap {sub}: {sub_exc}")

                return self.collected

            for url in locs:
                if len(self.collected) >= self.MAX_GUIDES:
                    break
                if self._is_relevant_doc(url):
                    self.collected.append(url)

            return self.collected

        except Exception as exc:
            self.logger.exception(f"Error fetching sitemap {sitemap_url}: {exc}")
            print(f"Error fetching sitemap {sitemap_url}: {exc}")
            return self.collected

    def _is_relevant_doc(self, url: str) -> bool:
        """
        Return True for AWS service pages that should be ingested:
        - User Guide
        - Developer Guide
        - API Reference
        - Best Practices Guide
        """
        return any(
            seg in url
            for seg in [
                "/latest/userguide/",
                "/latest/developerguide/",
                "/latest/APIReference/",
                "/latest/bestpracticesguide/",
            ]
        )

    async def ingest_all_aws_docs(self):
        """
        Discover every AWS service user-guide URL via sitemap,
        then bulk ingest under tenant 'AWS'.
        """

        self.logger.info("Ingestion Process Started")

        all_urls = self._fetch_sitemap()

        self.logger.info("Fetching Sitemap Process completed")

        guides = [u for u in all_urls if self._is_relevant_doc(u)]

        if len(guides) > self.MAX_GUIDES:
            guides = guides[: self.MAX_GUIDES]

        self.logger.info("Ingesting all Guides at once")
        await Ingestion.ingest_docs("AWS", guides)

    async def load(self, url: str) -> str:
        """
        Fetches and extracts text from an AWS documentation page.
        """
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        content = "\n".join([p.text for p in soup.find_all("p")])
        return content


# async def main():
#     """method for Unit testings and to run modules Independently."""

#     print(f" AWS Docs Crawling and Ingestion started")
#     aws_loader = AWSLoader()

#     asyncio.run(aws_loader.ingest_all_aws_docs())

# if __name__ == '__main__':
#     asyncio.run(main())
