# summarizer.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(text, level="basic"):
    prompt_map = {
        "basic": f"Summarize the following academic text:\n{text}",
        "bullet": f"Summarize this educational content into clear bullet points:\n{text}",
        "simple": f"Explain this study material like I'm a 12-year-old:\n{text}"
    }

    messages = [
        {"role": "system", "content": "You are a helpful tutor for students preparing for exams."},
        {"role": "user", "content": prompt_map.get(level, prompt_map["basic"])}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()