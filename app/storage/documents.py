import json
import os
from typing import Optional,Dict

DATA_DIR="data/registry"
REGISTRY_FILE=os.path.join(DATA_DIR,"documents.json")

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
        "status":status
    }

    _save_resgitry(registry)

def update_document_status(document_id:str,status:str):

    registry=_load_registry()
    if document_id not in registry:
        raise ValueError("Document not found")
    
    registry[document_id]["status"]=status

    _save_resgitry(registry)

def get_document(document_id:str)->Optional[Dict]:
    registry= _load_registry()
    return registry.get(document_id)    