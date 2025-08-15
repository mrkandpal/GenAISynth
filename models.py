#This file holds all the Pydantic models and enables reusability across modules
from pydantic import BaseModel

#input model for user prompt
class PromptRequest(BaseModel):
    prompt: str

#output model for synth parameters
class SynthParameters(BaseModel):
    oscillator :str
    cutoff :float
    resonance :float