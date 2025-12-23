from typing import List,Dict
from pypdf import PdfReader
from io import BytesIO


def load_pdf_text(file_bytes:BytesIO)->List[Dict]:

     reader=PdfReader(file_bytes)
     pages_data=[]
     for index ,page in enumerate(reader.pages):
       page_text=page.extract_text() or ""

       pages_data.append({
                "page_number":index+1,
                "text":page_text.strip()
            }) 

     return pages_data       
    

   
       
   

       