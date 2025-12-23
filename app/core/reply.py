from app.llm.groq_ll import generate_answer
from app.llm.context_builder import  build_context
from app.retrieval.finalRetrieval import query_document
from app.core.prompts import SYSTEM_PROMPT


def reply_by_llm(document_id:str,query:str)->str:

    top_chunks=query_document(document_id=document_id,query=query)
    context=build_context(top_chunks)

    user_prompt=f"""question: {query}
                     context:{context}
                     Answer:
                     """
    
    return generate_answer(SYSTEM_PROMPT,user_prompt)