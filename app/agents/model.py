from pydantic import BaseModel
from . import (
    get_prompt,
    get_model,
    get_response
)

class AgentInput(BaseModel):
    problem_title: str
    problem_description: str
    is_sandbox: bool
    student_code: str
    user_message: str
    chat_history: list[dict[str, str]]

def generate_ai_response(student_session, user_message, problem, student_code):
    prompt = get_prompt(
        problem_title=problem.title, 
        problem_description=problem.description, 
        is_sandbox=problem.is_sandbox, 
        student_code=student_code, 
        user_message=user_message,
        chat_history=student_session.chat_history
    )
    brain = get_model(TASK_DIFFICULTY = "LOW")
    config = {"configurable": {"session_id": student_session.id}}
    response = get_response(prompt, config, brain)
    
    return response

