import requests
# API kljuc za GPT API

CHATGPT_API_KLJUC = "sk-xxxxx"
api_url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHATGPT_API_KLJUC}",
}


def poslji_gpt_api(sporocila):

    try:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": sporocila
        }
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Klic na API ni uspel: \n{response.json()['error']['message']}"
    except requests.RequestException as e:
        return f"Klic na API ni uspel: \n{e}"
