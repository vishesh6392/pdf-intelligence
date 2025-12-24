from fastapi import APIRouter, HTTPException
from app.storage.documents import get_document

router = APIRouter()

@router.get("/document/{document_id}")
def get_document_status(document_id: str):
    doc=document_id.strip()
    doc = get_document(doc)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "document_id": doc["document_id"],
        "status": doc["status"]
    }
