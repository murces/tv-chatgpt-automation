import os
import base64
import openai
from dotenv import load_dotenv

load_dotenv()  # .env’den OPENAI_API_KEY okur
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
    resp = openai.ChatCompletion.create(
        model="o4-mini",
        messages=messages
    )
    return resp.choices[0].message.content.strip()
