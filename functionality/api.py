from openai import OpenAI
from .api_kljuc import CHATGPT_API_KLJUC

client = OpenAI(api_key=CHATGPT_API_KLJUC)

def poslji_gpt_api(sporocila):    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=sporocila
    )
    api_odgovor = completion.choices[0].message.content
    return api_odgovor
