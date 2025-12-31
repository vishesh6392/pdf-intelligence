
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
            update_document_status(document_id, status="FAILED")
            return
        total_pages = len(pages)
        print(f"[INFO]extracted{len(pages)} pages from document {document_id}")
        
        BATCH_SIZE = 16
        MAX_CHUNKS_PER_PAGE = 50    
        batch_chunks: List[Dict] = []
        
        for page_index,page in enumerate(pages):

            if page_index % 5 == 0:
                update_document_status(
                    document_id,
                    status="processing",   # IMPORTANT: unchanged
                    progress={
                        "processed_pages": page_index,
                        "total_pages": total_pages
                    }
                )

            # Chunk only THIS page

            page_chunks = chunk_pages([page])[:MAX_CHUNKS_PER_PAGE]

            for chunk in page_chunks:
                batch_chunks.append(chunk)

                # 6️⃣ When batch is full → embed + index
                if len(batch_chunks) == BATCH_SIZE:
                    try:
                        embeddings = embed_chunks(batch_chunks)
                        build_faiss_index(
                            document_id=document_id,
                            embeddings=embeddings,
                            chunks=batch_chunks
                        )
                    except Exception as e:
                        # One bad batch should not kill the whole document
                        print(f"[WARN] Batch failed, skipping batch: {e}")
                    finally:
                        # Always free memory
                        batch_chunks.clear()

        # 6️⃣ Flush remaining chunks
        if batch_chunks:
            try:
                embeddings = embed_chunks(batch_chunks)
                build_faiss_index(
                    document_id=document_id,
                    embeddings=embeddings,
                    chunks=batch_chunks
                )
            except Exception as e:
                print(f"[WARN] Final batch failed: {e}")
            finally:
                batch_chunks.clear()

        update_document_status(
            document_id,
            status="processing",
            progress={
                "processed_pages": total_pages,
                "total_pages": total_pages
            }
        )



        update_document_status(document_id,status="Ready")
        print(f"success , document {document_id} indexed and ready")

    except Exception as e:
      print(f"[ERROR] Ingestion failed for document {document_id}")
      traceback.print_exc()
      update_document_status(document_id, status="FAILED")