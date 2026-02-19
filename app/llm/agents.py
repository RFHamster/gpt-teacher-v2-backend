from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os

def get_model(model_name: str):
    models_config = {
        "Groq": get_grok,
        "GPT": get_gpt
    }
    
    constructor = models_config.get(model_name)
    
    if not constructor:
        raise ValueError(f"Modelo {model_name} não suportado.")
        
    return constructor() 

def get_grok():
    return ChatGroq(
            model="llama-3.1-8b-instant", 
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

def get_gpt():
    return ChatOpenAI(
            model="gpt-4o", 
            api_key=os.getenv("OPENAI_API_KEY")
        )