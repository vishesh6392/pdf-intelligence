import os 
import json 
from typing import List,Dict

import faiss

def build_faiss_index(document_id:str,embeddings,chunks:List[Dict])->None:
    if len(embeddings)==0:
        raise ValueError("no embeddings provided")
    
    dim = embeddings.shape[1]

    index=faiss.IndexFlatIP(dim)
    index.add(embeddings)

    index_dir=os.path.join("data","index",document_id)
    os.makedirs(index_dir,exist_ok=True)

    index_path=os.path.join(index_dir,"faiss.index")
    metadata_path=os.path.join(index_dir,"meta.json")

    faiss.write_index(index,index_path)
    metadata=[]

    for i,chunk in enumerate(chunks):
        metadata.append({
            "vector_id":i,
            "chunk_id":chunk["chunk_id"],
            "page_number": chunk["page_number"],
            "text":chunk["text"]
        })

    with open(metadata_path,"w",encoding="utf-8") as f:
        json.dump(metadata,f,indent=2)

    print(f"[INFO] Faiss index build for document {document_id}")        
