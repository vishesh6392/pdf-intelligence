# from app.ingestion.loader.pdf_text_loader import load_pdf_text

# data = load_pdf_text("data/raw/950c457f-5861-4e52-bfe1-3bb3195d97a0.pdf")

# print(data[0]["page_number"])
# print(data[0]["text"][:500])


# from app.ingestion.worker import ingest_documnents

# ingest_documnents("950c457f-5861-4e52-bfe1-3bb3195d97a0")

# from app.ingestion.loader.pdf_text_loader import load_pdf_text
# from app.ingestion.chunker import chunk_pages

# pages = load_pdf_text("data/raw/950c457f-5861-4e52-bfe1-3bb3195d97a0.pdf")
# chunks = chunk_pages(pages)

# print("Total chunks:", len(chunks))
# print(chunks[0])

# from app.ingestion.worker import ingest_documnents

# ingest_documnents("96e20624-0804-4736-a7ab-2b899595a7df")

# from app.retrieval.search import semantic_search

# DOC_ID = "950c457f-5861-4e52-bfe1-3bb3195d97a0"

# results = semantic_search(
#     document_id=DOC_ID,
#     query="Explain eigenvalues in simple words",
#     top_k=5
# )

# for r in results:
#     print(f"Page {r['page_number']} | Score {r['score']:.3f}")
#     print(r["text"][:200])
#     print("-" * 40)
# from app.core.reply import reply_by_llm   # adjust path if filename differs

# DOCUMENT_ID = "96e20624-0804-4736-a7ab-2b899595a7df"
# QUERY = "What is eigenvalue?"

# answer = reply_by_llm(
#     document_id=DOCUMENT_ID,
#     query=QUERY
# )

# print("\n===== FINAL ANSWER =====\n")
# print(answer)
 
from app.storage.documents import get_document

print( get_document("c7a3024a-dc77-4b69-bd6c-c746f50e7b68"))



