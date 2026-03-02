from app.agents import get_prompt
from enum import Enum

class GroqModels(str, Enum):
    LLAMA_3_3_8b = "llama-3.3-8b"
    LLAMA_3_3_70b_VERSATILE = "llama-3.3-70b-versatile"
    MIXTRAL_8X7B_32768 = "mixtral-8x7b-32768"

MODEL_BY_DIFICULTY = {
    'LOW': GroqModels.LLAMA_3_3_8b,
    'MEDIUM': GroqModels.LLAMA_3_3_70b_VERSATILE,
    'HIGH': GroqModels.MIXTRAL_8X7B_32768
}

def get_groq_model(task_dificulty: str):
    model = MODEL_BY_DIFICULTY.get(task_dificulty, None)
    
    if not model:
        raise ValueError("Model not Found")
    
    return model
