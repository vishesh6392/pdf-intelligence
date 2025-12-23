from app.retrieval.search import semantic_search
from app.reranking.reranker import CrossEncoderReranker


reranker=CrossEncoderReranker()

def query_document(document_id:str,query:str):

    chunks=semantic_search(document_id=document_id,query=query,top_k=20)
    reranked_chunks=reranker.rerank(query=query,chunks=chunks,top_k=5)

    return reranked_chunks