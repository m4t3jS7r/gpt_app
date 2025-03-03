import requests
# API kljuc za GPT API

CHATGPT_API_KLJUC = "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"
api_url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHATGPT_API_KLJUC}",
}


def poslji_gpt_api(sporocila):

    try:
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": sporocila
        }
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Klic na API ni uspel: \n{response.json()['error']['message']}"
    except requests.RequestException as e:
        return f"Klic na API ni uspel: \n{e}"
