from typing import List,Dict

def build_context(chunks:List[Dict])->str:

    context_blocks=[]
    for i,chunk in enumerate(chunks,start=1):
        block=f"""[source {i}]
                   page:{chunk.get("page_number")}
                   content:{chunk.get("text")}
        """
        context_blocks.append(block.strip())
        
    return "\n\n".join(context_blocks)    
    