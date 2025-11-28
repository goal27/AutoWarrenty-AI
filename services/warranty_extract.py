import openai
import json

def extract_warranty_structured(text, system_prompt, current_date):
    """
    Core LLM call for final structured JSON using WarrantyGen system prompt.
    """
    user_content = f"{text}\n\nCurrent Date: {current_date}"
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.1,
        max_tokens=3000
    )

    content = response.choices[0].message.content.strip()

    # Auto-fix JSON blocks
    if content.startswith("```"):
        content = content.split("```")[1].strip()

    try:
        result = json.loads(content)
        return result
    except Exception as e:
        return {"error": "Invalid JSON returned", "raw": content}
