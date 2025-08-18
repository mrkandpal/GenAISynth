#This file holds all the Pydantic models and enables reusability across modules
from pydantic import BaseModel, Field

#input model for user prompt
class PromptRequest(BaseModel):
    prompt: str

#output model for ADSR
class Envelope(BaseModel):
    attack: float = Field()
    decay:float = Field()
    sustain:float = Field()
    release:float = Field()

#output model for synth parameters
class SynthParameters(BaseModel):
    oscillator :str
    cutoff :float
    resonance :float