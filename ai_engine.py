# ai_engine.py
import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODEL = "mistralai/mistral-7b"

def generate_reply(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالنموذج: {e}"
