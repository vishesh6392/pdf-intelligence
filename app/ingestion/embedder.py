from typing import List,Dict
import numpy as np
from sentence_transformers import SentenceTransformer


Model_Name="all-MiniLm-L6-v2"
_model=SentenceTransformer(Model_Name)

def embed_chunks(chunks:List[Dict])->np.ndarray:
    if not chunks:
        raise ValueError("No chunks provided for embedding")
    
    texts=[chunk["text"] for chunk in chunks]

    embeddings=_model.encode(texts,show_progress_bar=True,normalize_embeddings=True)
    return embeddings