from fastapi import BackgroundTasks

from src.backend.core.logger import get_logger
from src.backend.docs_engine.loaders.aws_loaders import AWSLoader
from src.backend.docs_engine.retriver import retrieve_relevant_chunks


class DocEngineService:

    doc_logger = get_logger("doc_engine_service")

    @classmethod
    def sync_docs(cls, doc_name: str, background_tasks: BackgroundTasks):

        cls.doc_logger.info(f"Starting background syncing process for {doc_name} docs")

        aws_loader = AWSLoader(logger=cls.doc_logger)
        background_tasks.add_task(aws_loader.ingest_all_aws_docs)

        return {"message": f"Started background syncing process for {doc_name} docs"}

    @classmethod
    def ret_docs(cls, query: str, tenant: str):
        res = retrieve_relevant_chunks(query, tenant)
        return res
