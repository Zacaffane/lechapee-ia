from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_wikisource_page(raw_text: str):
    from app.prompts.wikisource_prompt import PROMPT_ANALYSE_WIKISOURCE

    prompt = PROMPT_ANALYSE_WIKISOURCE.replace("{{{CONTENU_BRUT_WIKISOURCE}}}", raw_text[:8000])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un expert de Wikisource et de la littérature classique."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content
