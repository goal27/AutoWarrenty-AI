import openai
import json
import os

def analyze_problem_with_warranty(problem_description, warranty_details):
    with open("prompts/agent_problem_analysis.txt", "r") as f:
        system_prompt = f.read()

    user_content = f"Problem Description: {problem_description}\n\nWarranty Details: {json.dumps(warranty_details, indent=2)}"

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
