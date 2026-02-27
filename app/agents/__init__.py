from agent_groq.prompt import SYSTEM_PROMPT
from model import AgentInput
from agent_groq.groq_agent import get_groq_model, get_response_from_groq_model

def get_prompt(agent_input: AgentInput):
    return SYSTEM_PROMPT.format(
        problem_title=agent_input.problem_title,
        problem_description=agent_input.problem_description,
        is_sandbox=agent_input.is_sandbox,
        student_code=agent_input.student_code,
        user_message=agent_input.user_message,
        chat_history=agent_input.chat_history
    )

def get_model(TASK_DIFFICULTY):
    return get_groq_model(TASK_DIFFICULTY)

def get_response(prompt, config, brain):
    return get_response_from_groq_model(prompt, config, brain)