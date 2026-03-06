from app.agents import get_model_by_difficulty
from app.agents.teacher_agent.prompt import SYSTEM_PROMPT
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.language_models import BaseChatModel
from langchain.agents import create_agent
from app.agents.teacher_agent.model import AgentInput

def get_prompt(agent_input: AgentInput) -> ChatPromptValue:
    return SYSTEM_PROMPT.invoke({
        "problem_title": agent_input.problem_title,
        "problem_description": agent_input.problem_description,
        "is_sandbox": agent_input.is_sandbox,
        "student_code": agent_input.student_code,
        "user_message": agent_input.user_message,
        "chat_history": agent_input.chat_history
    })

def get_model(TASK_DIFFICULTY: str, tools: list[str]) -> BaseChatModel:
    model = get_model_by_difficulty(TASK_DIFFICULTY)
    
    return create_agent(
        model=model,
        tools=tools
    )