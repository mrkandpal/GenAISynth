import subprocess
import json
from fastapi import HTTPException

def generate_synth_params_local(user_prompt: str, fallback_on_error: bool = True):
    """
    Calls the local Ollama Mistral model via CLI and returns SynthParameters dict. 
    """

    try:
        #run ollama CLI command
        result = subprocess.run(
            ["ollama", "run", "mistral", "--prompt", user_prompt],
            capture_output=True,
            text=True,
            check=True
        )

        #Store result as raw text
        raw_text = result.stdout.strip()

        #Remove JSON fences if present
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()

        # Parse JSON
        try:
            params = json.loads(raw_text)
        except json.JSONDecodeError:
            if fallback_on_error:
                params = {"oscillator": "sine", "cutoff": 1000.0, "resonance": 0.5}
            else:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid JSON from local LLM: {raw_text}"
                )

    except subprocess.CalledProcessError as e:
        if fallback_on_error:
            return {"oscillator": "sine", "cutoff": 1000.0, "resonance": 0.5}
        raise HTTPException(
            status_code=500,
            detail=f"Local LLM call failed: {str(e)}"
        )
    
    return params
