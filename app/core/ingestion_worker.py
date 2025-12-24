import time
import traceback
from app.storage.documents import (
    get_documents_by_status,
    update_document_status
)
from app.ingestion.worker import ingest_documnents

POLL_INTERVAL = 15  # seconds (safe for free tier)

def run_worker():
    print("[WORKER] Ingestion worker started")

    while True:
        try:
            # 1️⃣ Fetch all processing documents
            processing_docs = get_documents_by_status("processing")

            if not processing_docs:
                time.sleep(POLL_INTERVAL)
                continue

            print(f"[WORKER] Found {len(processing_docs)} documents to process")

            for document_id in processing_docs:
                try:
                    print(f"[WORKER] Ingesting document {document_id}")

                    # 2️⃣ Run ingestion (idempotent)
                    ingest_documnents(document_id)

                except Exception as e:
                    print(f"[WORKER][ERROR] Failed document {document_id}")
                    traceback.print_exc()

                    # 3️⃣ Mark failed safely
                    update_document_status(document_id, "failed")

            time.sleep(POLL_INTERVAL)

        except Exception as e:
            print("[WORKER][FATAL] Worker loop crashed, restarting...")
            traceback.print_exc()
            time.sleep(5)  # small backoff

if __name__ == "__main__":
    run_worker()
