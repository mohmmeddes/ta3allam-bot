# ai_engine.py
from transformers import pipeline

# تحميل نموذج توليد نصوص خفيف يدعم العربية
generator = pipeline("text2text-generation", model="google/flan-t5-small")

def generate_reply(prompt: str) -> str:
    try:
        response = generator(prompt, max_length=100, do_sample=True)[0]['generated_text']
        return response.strip()
    except Exception as e:
        return f"حدث خطأ في المعالجة: {e}"
