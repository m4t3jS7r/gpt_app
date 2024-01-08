import requests
# API kljuc za GPT API

CHATGPT_API_KLJUC = "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"
api_url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHATGPT_API_KLJUC}",
}


def poslji_gpt_api(sporocila):

    data = {
        "model": "gpt-3.5-turbo",
        "messages": sporocila
    }
    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Klic na API ni uspel, poskusi znova?"
