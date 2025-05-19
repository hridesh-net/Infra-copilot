# rag_agent/aws_crawler.py
import requests
import xml.etree.ElementTree as ET
import asyncio
import logging
from xml.etree.ElementTree import ParseError
from rag_agent.doc_manager import ingest_docs

# Maximum number of AWS docs to ingest in this run (for quick testing)
MAX_GUIDES = 10

AWS_SITEMAP_INDEX = "https://docs.aws.amazon.com/sitemap_index.xml"

logger = logging.getLogger(__name__)

# Collected relevant docs, across recursive calls
collected: list[str] = []


def fetch_sitemap(sitemap_url: str) -> list[str]:
    """
    Download and parse a sitemap or sitemap-index, returning all <loc> URLs.
    Recurses if this is a sitemapindex.
    Handles non-XML and parse errors gracefully.
    """
    # If we've reached our ingestion limit, stop further crawling
    if len(collected) >= MAX_GUIDES:
        return collected

    try:
        resp = requests.get(sitemap_url, timeout=30)
        resp.raise_for_status()
        content_type = resp.headers.get('Content-Type', '')
        print(f"content type: {content_type}, for URL: {sitemap_url}")
        if 'xml' not in content_type:
            logger.warning(f"Skipping non-XML at {sitemap_url}, treating as doc if applicable")
            if any(seg in sitemap_url for seg in [
                '/latest/userguide/',
                '/latest/developerguide/',
                '/latest/APIReference/',
                '/latest/bestpracticesguide/'
            ]):
                if len(collected) < MAX_GUIDES:
                    collected.append(sitemap_url)
                return collected
            return collected
        try:
            root = ET.fromstring(resp.text)
        except ParseError as e:
            logger.warning(f"Failed to parse XML sitemap {sitemap_url}: {e}")
            return collected
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [elem.text for elem in root.findall('.//sm:loc', ns)]
        if root.tag.lower().endswith('sitemapindex'):
            for sub in locs:
                if len(collected) >= MAX_GUIDES:
                    break
                try:
                    fetch_sitemap(sub)
                except Exception as sub_exc:
                    logger.warning(f"Error fetching sub-sitemap {sub}: {sub_exc}")
            return collected
        # urlset
        # Collect only relevant docs up to our limit
        for url in locs:
            if len(collected) >= MAX_GUIDES:
                break
            if is_relevant_doc(url):
                collected.append(url)
        return collected
    except Exception as exc:
        logger.warning(f"Error fetching sitemap {sitemap_url}: {exc}")
        return collected


def is_relevant_doc(url: str) -> bool:
    """
    Return True for AWS service pages that should be ingested:
    - User Guide
    - Developer Guide
    - API Reference
    - Best Practices Guide
    """
    return any(
        seg in url for seg in [
            "/latest/userguide/",
            "/latest/developerguide/",
            "/latest/APIReference/",
            "/latest/bestpracticesguide/"
        ]
    )


def ingest_all_aws_docs():
    """
    Discover every AWS service user-guide URL via sitemap,
    then bulk ingest under tenant 'AWS'.
    """
    print("Fetching AWS sitemap index...")
    all_urls = fetch_sitemap(AWS_SITEMAP_INDEX)
    print(f"Discovered {len(all_urls)} URLs; filtering to user guides...")

    guides = [u for u in all_urls if is_relevant_doc(u)]
    # Limit the number of guides to crawl/page-fetch to save time
    if len(guides) > MAX_GUIDES:
        print(f"Limiting to first {MAX_GUIDES} guides out of {len(guides)} discovered")
        guides = guides[:MAX_GUIDES]
    print(f"{len(guides)} user-guide URLs to ingest.")

    # Run ingestion pipeline for all guides under topic 'AWS'
    print("sending to ingest docs")
    asyncio.run(ingest_docs("AWS", guides))


if __name__ == '__main__':
    ingest_all_aws_docs()
