from fastapi import APIRouter, BackgroundTasks

from src.backend.services.docs_engine import DocEngineService

doc_router = APIRouter()


@doc_router.get("/sync_docs/{doc_name}")
async def sync_docs(doc_name: str, background_tasks: BackgroundTasks):
    resp = DocEngineService.sync_docs(doc_name=doc_name, background_tasks=background_tasks)
    return resp
