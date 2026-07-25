from app.agents.teacher_agent.model import AgentInput
from app.agents.teacher_agent import call_teacher_agent


def generate_ai_response(agent_input: AgentInput) -> str:
    return call_teacher_agent(agent_input)