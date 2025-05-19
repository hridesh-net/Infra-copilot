import click
import asyncio

from rag_agent.doc_manager import ingest_docs
from rag_agent.orchestrator import retrieve_and_ask

@click.group()

def cli():
    """RAG Agent CLI for doc ingestion and querying."""
    pass

@cli.command()
@click.option('--topic', required=True, help='Topic name, e.g., AWS, Azure, Terraform')
@click.option('--url', 'urls', required=True, multiple=True, help='Documentation URL(s) to ingest')
def ingest(topic, urls):
    """Ingest official docs for a given topic."""
    asyncio.run(ingest_docs(topic, list(urls)))
    click.echo(f"Ingestion for topic '{topic}' completed.")

@cli.command()
@click.option('--topic', required=True, help='Topic name to use for retrieval')
@click.option('--query', required=True, help='User question')
def ask(topic, query):
    """Retrieve context and ask the LLM."""
    answer = asyncio.run(retrieve_and_ask(topic, query))
    click.echo(answer)

if __name__ == '__main__':
    cli()
