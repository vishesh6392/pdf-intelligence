import os 
from groq import Groq 
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GROQ_API_KEY")
print("Groq key loaded:", repr(key))


client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(system_prompt:str,user_prompt:str)->str:
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt},
        ],
        temperature=0.3,
        max_tokens=700
    )
    content= response.choices[0].message.content or ""
    return content.strip()

