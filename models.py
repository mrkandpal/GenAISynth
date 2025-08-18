#This file holds all the Pydantic models and enables reusability across modules
from pydantic import BaseModel, Field

#input model for user prompt
class PromptRequest(BaseModel):
    prompt: str

#output model for synth parameters
class SynthParameters(BaseModel):
    oscillator :str = Field(..., descripton="Oscillator type: sine, square, saw, triangle")
    cutoff :float = Field(..., gt=20.0, lt=20000.0,description="Filter cutoff freuency in Hz")
    resonance :float = Field(...,ge=0.1,le=5.0,description="Filter resonance (Q Factor)")
    atatck: float = Field(...,ge=0.0,le=5.0,description="Envelope attack time in seconds")
    decay: float = Field(...,ge=0.0,le=5.0,description="Envelope decay time in seconds")
    sustain: float = Field(...,ge=0.0,le=1.0,description="Envelope sustaio time in seconds")
    release: float = Field(...,ge=0.0,le=5.0,description="Envelope release time in seconds")
    gain:float = Field(...,ge=0.0,le=1.0,description="Output gain [0-1]")

def synthparameters_json_schema() -> dict:
    """Return JSON Schema dict for validation """
    return SynthParameters.model_json_schema()