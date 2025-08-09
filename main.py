import os
import openai
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create a FastAPI app
app = FastAPI()

# openAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define a request model for the prompt
#PromptRequest is a Pydantic model class that defines LLM prompts to obtain synth parameters
class PromptRequest(BaseModel):
    prompt : str

#Define a request model for comparison between two genres
class CompareRequest(BaseModel):
    genre1 : str
    genre2 : str

#Define a response model for comparison between two genres

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

@app.post("/compare")
def compare(request : CompareRequest):
    #Test prototype - return fake comparison between two genres
    return{
        "genre1": request.genre1,
        "genre2": request.genre2,
        "comparison": "The two genres are similar in that they both use synthesizers and have a similar sound."
    }