import os 
import json
from  typing import List,Dict,Tuple

import faiss
import numpy as np

from app.ingestion.embedder import embed_chunks

def semantic_search(document_id:str,query:str,top_k :int=10)-> List[Dict]:

    index_dir=os.path.join("data","index",document_id)
    index_path=os.path.join(index_dir,"faiss.index")
    metadata_path=os.path.join(index_dir,"meta.json")

    if not os.path.exists(index_path):
        raise FileNotFoundError("Faiss index not found")
    
    index=faiss.read_index(index_path)
    with open(metadata_path,"r",encoding="utf-8") as f:
        metadata=json.load(f)

    query_embedding=embed_chunks([{
        "text":query
    }])  


    scores,indices=index.search(
        query_embedding.astype(np.float32),
        top_k
    )  

    results=[]
    for score,idx in zip(scores[0],indices[0]):
        if idx == -1:
            continue

        chunk_meta=metadata[idx]

        results.append({
            "chunk_id":chunk_meta["chunk_id"],
            "page_number":chunk_meta["page_number"],
            "text":chunk_meta["text"],
            "score":float(score)
        })
    return results    
