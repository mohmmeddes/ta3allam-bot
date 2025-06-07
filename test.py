import openai
import os

# إعداد المفتاح ونقطة الوصول لـ OpenRouter
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def test_model():
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",  # هذا الذكاء اللي تستخدمه
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي"},
                {"role": "user", "content": "وش أفضل طرق تنظيم الوقت؟"}
            ]
        )
        print("✅ الرد من الذكاء:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("❌ فيه مشكلة في الاتصال بالذكاء الاصطناعي:")
        print(e)

if __name__ == "__main__":
    test_model()