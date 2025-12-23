
from typing import List,Dict
import traceback
from app.storage.s3 import download_pdf
from app.ingestion.loader.pdf_text_loader import load_pdf_text
from app.storage.documents import update_document_status
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import embed_chunks
from app.ingestion.indexer import build_faiss_index

def ingest_documnents(document_id:str)-> None:
    try:
        update_document_status(document_id,status="processing")


        s3_key=f"raw/{document_id}.pdf"
        pdf_bytes=download_pdf(s3_key)
        


        pages:List[Dict]=load_pdf_text(pdf_bytes)
        if not pages:
            print(f"[WARN] no text extracted for document {document_id}")
        print(f"[INFO]extracted{len(pages)} pages from document {document_id}")

        chunks=chunk_pages(pages)
        if not chunks:
            raise ValueError("chunking produce not chunk")
        print(f"created {len(chunks)} chunks")


        embeddings=embed_chunks(chunks)
        if  embeddings.size == 0:
            raise ValueError("embedding fails")
        print(f"generated embedding with sphape {embeddings.shape}")
        

        build_faiss_index( document_id=document_id,embeddings=embeddings,chunks=chunks)

        update_document_status(document_id,status="Ready")

        print(f"success , document {document_id} indexed and ready")

    except Exception as e:
      print(f"[ERROR] Ingestion failed for document {document_id}")
      traceback.print_exc()
      update_document_status(document_id, status="FAILED")