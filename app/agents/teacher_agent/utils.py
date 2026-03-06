from app.agents.teacher_agent.model import AgentInput
from . import get_model, get_prompt

def generate_ai_response(agent_input: AgentInput) -> str:
    prompt = get_prompt(agent_input)

    brain = get_model(
        TASK_DIFFICULTY = "LOW", 
        tools=[]
    )
    
    response = brain.invoke({"messages": prompt.to_messages()})
    
    return response.content