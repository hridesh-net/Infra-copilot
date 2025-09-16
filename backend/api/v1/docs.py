from fastapi import APIRouter, BackgroundTasks

from src.backend.services.docs_engine import DocEngineService

doc_router = APIRouter()


@doc_router.get("/sync_docs/{doc_name}")
async def sync_docs(doc_name: str, background_tasks: BackgroundTasks):
    resp = DocEngineService.sync_docs(doc_name=doc_name, background_tasks=background_tasks)
    return resp


@doc_router.get("ret_doc/{query}")
async def ret_doc(query: str, tenant: str = "AWS"):
    resp = DocEngineService.ret_docs(query=query, tenant=tenant)
    return resp
