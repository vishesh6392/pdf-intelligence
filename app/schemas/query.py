from pydantic import BaseModel

class queryRequest(BaseModel):
    document_id:str
    query:str

class queryResponse(BaseModel):
    document_id:str
    query:str
    answer:str
        