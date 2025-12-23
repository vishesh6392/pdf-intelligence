from fastapi import APIRouter,HTTPException

from app.schemas.query import queryRequest,queryResponse
from app.core.reply import reply_by_llm
from app.storage.documents import get_document

router=APIRouter()

@router.post("/query",response_model=queryResponse)
def query_doc_api(payload:queryRequest):
    doc=get_document(payload.document_id)
    if not doc:
        raise HTTPException(status_code=404,detail="doc not found")
    
    if doc["status"].lower()!="ready":
        raise HTTPException(status_code=400,detail=f"doc status is{doc['status']},not ready for query")
    
    try:
        ans=reply_by_llm(document_id=payload.document_id,query=payload.query)
    except Exception as e:
        raise HTTPException(status_code=500,detail="failed to generate answer")

    return queryResponse(
        document_id=payload.document_id,
        query=payload.query,
        answer=ans
    )    
