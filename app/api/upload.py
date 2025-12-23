from fastapi import APIRouter ,UploadFile,File,BackgroundTasks,HTTPException
import uuid

# from app.ingestion.worker import ingest_document
from app.storage.documents import create_document
from app.storage.s3 import upload_pdf

router=APIRouter()

@router.post("/upload")
async def upload_doc(file:UploadFile=File(...)):
    
    doc_id=str(uuid.uuid4())

    s3_key=f"raw/{doc_id}.pdf"
    upload_pdf(file.file,s3_key)


    create_document(document_id=doc_id,filename=file.filename or "unknown.pdf",status="processing")   

    
    return {
        "document_id": doc_id,
        "status": "PROCESSING",
        "message": "PDF uploaded successfully"
    }
 


