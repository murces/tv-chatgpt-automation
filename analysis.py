import os
import base64
import openai
from dotenv import load_dotenv
from openai.error import RateLimitError, OpenAIError

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_images(images):
    prompt_header = (
        "Her coin için 5m, 1h ve 4h son kapanış bar grafiklerini aşağıda bulacaksınız.\n"
        "Herhangi bir coin’de long (uzun) veya short (kısa) pozisyon fırsatı var mı?\n"
        "Eğer evet:\n"
        "- Pozisyon tipi (long/short)\n"
        "- Giriş fiyatı\n"
        "- TP (take profit) ve SL (stop loss) seviyeleri\n"
        "Eğer hiçbir fırsat yoksa, “<coin> için şu anda fırsat yok.” deyin.\n\n"
    )

    messages = [{"role": "system", "content": prompt_header}]

    for img in images:
        with open(img["path"], "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        messages.append({
            "role": "user",
            "content": f"{img['symbol']} {img['tf']} grafiği:",
            "image": {"data": b64}
        })

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
        return f"Bir hata oluştu: {e.user_message or e}"
