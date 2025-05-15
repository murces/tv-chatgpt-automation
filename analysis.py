import os
import base64
import openai
from dotenv import load_dotenv
from openai.error import RateLimitError, OpenAIError

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_image(image_path: str, prompt_text: str) -> str:
    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode()

    messages = [
        {
            "role": "user",
            "content": prompt_text,
            "image": {"data": img_b64}
        }
    ]
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return resp.choices[0].message.content.strip()
    except RateLimitError:
        return ("Üzgünüm, şu anda kota limitime ulaştım ve analiz yapamıyorum. "
                "Lütfen planınızı kontrol edin veya biraz sonra tekrar deneyin.")
    except OpenAIError as e:
        # Diğer API hataları için genel bir mesaj
        return f"Bir hata oluştu: {e.user_message or e}"
