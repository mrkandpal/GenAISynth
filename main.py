#This is the fastapi entry point
from fastapi import FastAPI
from models import PromptRequest, SynthParameters
from services.llm_service import generate_synth_params

app = FastAPI()

@app.post("/synthesize", response_model = SynthParameters)
async def synthesize(request: PromptRequest):
    """
    Takes a user prompt, sends it to the LLM, 
    and returns validated synthesizer parameters.
    """
    return generate_synth_params(request.prompt)

