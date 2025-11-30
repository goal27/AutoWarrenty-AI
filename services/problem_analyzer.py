import openai
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

def analyze_problem_with_warranty(problem_description, warranty_details):
    with open("prompts/agent_problem_analysis.txt", "r") as f:
        system_prompt = f.read()

    current_date = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
    user_content = (
        f"Problem Description: {problem_description}\n\n"
        f"Warranty Details: {json.dumps(warranty_details, indent=2)}\n\n"
        f"Current Date: {current_date}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error analyzing problem: {e}")
        return None
