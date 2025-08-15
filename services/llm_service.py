#This is a dedicated service layer for LLM calls
#Keeps logic separate from API routes

import os
import json
from fastapi import HTTPException
from openai import OpenAI
from models import SynthParameters

PROMPT_TEMPLATE = """
Generate synthesizer parameters in JSON format:
oscillator: string
cutoff: float
resonance: float

User prompt: {user_prompt}
"""

#Initialize OpenAI client with API key from environment
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def generate_synth_params(user_prompt: str, fallback_on_error:bool = True) -> SynthParameters:
    #Build the prompt
    prompt = PROMPT_TEMPLATE.format(user_prompt=user_prompt)

    # Generate response using OpenAI gpt-4o-mini
    try:
        #Call the openAI APIra
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [{"role" : "user", "content" : prompt}],
            max_tokens = 200,
            temperature = 0.7
        )

        # Extract text from the first choice
        raw_text = response.choices[0].message.content.strip()

        # Parse the JSON response
        # Handle fences - lean up the response if it contains markdown code blocks
        if "```json" in raw_text:
            # Split response string text between the '''json...''' fence
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            # Split response string text between the '''...''' fence
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
                
        try:
            # Parse JSON from cleaned up text    
            params = json.loads(raw_text)
        except json.JSONDecodeError as e:
            # Log the raw text for debugging
            print(f"[Warning] Malformed JSON received: {raw_text}")
            if fallback_on_error:
                # Use default parameters
                params = {"oscillator": "sine", "cutoff": 1000.0, "resonance": 0.5}
            else:
                # Raise HTTPException for invalid JSON
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid JSON from LLM: {str(e)}"
                )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate synthesizer parameters: {str(e)}")

# Validate with Pydantic and return
    return SynthParameters(**params)