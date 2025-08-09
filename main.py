import os
import openai
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create a FastAPI app
app = FastAPI()

# openAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a request model for the prompt
#PromptRequest is a Pydantic model class that defines LLM prompts to obtain synth parameters
class PromptRequest(BaseModel):
    prompt : str

# Define a response model for the prompt
#This model is at an experimental stage for now.... The exact structure will evenetually depend on the JUCE synthesizer
class SynthParameters(BaseModel):
    oscillator : str
    cutoff : float
    resonance : float

#Prompt Template for instructing LLM to return JSON
PROMPT_TEMPLATE = """
You are synthesizer parameter generator. Given a user prompt, respond only with JSON in the following format:
{{
    "osciallator" : "sine" | "saw" | "square" | "triangle",
    "cutoff" : 20 to 20000,
    "resonance" : 0.0 to 1.0
}}

User prompt: "{user_prompt}"

"""

#GET route for testing API
@app.get("/")
def read_root():
    return {"message": "Hello from FASTApi"}

#POST route for generation of synthesizer parameters
"""
The endpoint /synthesize will return a JSON object with the synthesizer parameters.
Prompts may be generic or specfic 
For example, a generic prmopt could be, 
I want a synth that sounds like a 1980s synth

More specifically, a prompt can include a specific genre, instrument, or mood, like, 
I want a synth that resembles 1980s acid house

Prompts can also include names of specific synthesizers, like, 
I want a synth that sounds like a Yamaha DX7 or Roland TB-303

A prmopt may also include names of specific artists, like, 
I want a synth that sounds like the music of Daft Punk

"""
@app.post("/synthesize")
def synthesize(request: PromptRequest):
    # Test prototype - return fake synthesizer parameters
    return{
        "oscillator_type": "sawtooth",
        "cutoff_frequency": 1200,
        "resonance": 0.7,
        "received_prompt": request.prompt
    }

