import openai
from PIL import Image
import io
import base64
import os

def extract_text_from_image(image_file):
    """
    Uses GPT-4o-mini Vision to extract OCR text.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    image_bytes = image_file.read()
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all visible text clearly."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"}}
                ]
            }
        ]
    )

    return response.choices[0].message.content
