from typing import List,Dict

def chunk_pages(pages:List[Dict],chunk_size:int=800,overlap:int=200)->List[Dict]:

    chunks:List[Dict]=[]
    for page in pages:
        page_number=page["page_number"]
        text=page["text"]

        if not text:
            continue
        start=0
        chunk_index=0
        while start<len(text):
            end=start+chunk_size
            chunk_text=text[start:end]
            chunks.append({
                "chunk_id":f"p{page_number}_c{chunk_index}",
                "page_number":page_number,
                "text":chunk_text.strip()
            })
            start=end-overlap
            chunk_index+=1

    return chunks        