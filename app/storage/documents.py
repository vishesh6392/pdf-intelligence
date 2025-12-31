import json
import os
from typing import Optional,Dict


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
DATA_DIR=os.path.join(BASE_DIR, "data", "registry")
REGISTRY_FILE=os.path.join(DATA_DIR,"documents.json")

print("USING REGISTRY FILE:", REGISTRY_FILE)

os.makedirs(DATA_DIR,exist_ok=True)

def _load_registry() -> Dict:
    if not os.path.exists(REGISTRY_FILE):
        return {}
    with open(REGISTRY_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def _save_resgitry(data:Dict):
    with open(REGISTRY_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=2)

def create_document( document_id:str, filename:str,status:str):

    registry=_load_registry()

    registry[document_id]={
        "document_id":document_id,
        "filename":filename,
        "status":status,
        "progress":None
    }

    _save_resgitry(registry)

def update_document_status(document_id:str,status:str,progress:Optional[Dict]=None):

    registry=_load_registry()
    if document_id not in registry:
        raise ValueError("Document not found")
    
    registry[document_id]["status"]=status
    if progress is not None:
        registry[document_id]["progress"]=progress

    _save_resgitry(registry)

def get_document(document_id:str)->Optional[Dict]:
    registry= _load_registry()
    return registry.get(document_id)    

def get_documents_by_status(status: str):
    registry = _load_registry()
    return {
        doc_id: doc
        for doc_id, doc in registry.items()
        if doc["status"] == status
    }
