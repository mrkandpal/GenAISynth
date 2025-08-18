import json 
import logging
from fastapi import HTTPException
from openai import OpenAI
from prompt_template  import PROMPT_TEMPLATE

logger = logging.getLogger(__name__)
client = OpenAI()

def openai_generate_raw(user_prompt: str) -> dict:
    """Call OpenAi and return raw dict from JSON output"""

    try:
        prompt = PROMPT_TEMPLATE.format(user_prompt = user_prompt)

        response = client.chat.completions.create(
            model = "gpt-40-mini",
            messages = [{"role":"user","content":prompt}],
            max_tokens=200,
            temperature=0.7
        )

        raw_text = response.choices[0].message.content.strip()

        # Defensive stripping of code fences (e.g., ```json ... ```)
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()

        return json.loads(raw_text)
    
    except Exception as e:
        logger.exception("OpenAI generation failed")
        raise HTTPException(status_code=500, detail=f"OpenAI generation error: {str(e)}")