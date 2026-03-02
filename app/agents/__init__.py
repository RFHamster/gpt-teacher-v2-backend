from teacher_agent.prompt import SYSTEM_PROMPT
from app.agents.teacher_agent.model import AgentInput
from teacher_agent.teacher_agent import get_groq_model
from gpt_teacher_db.gpt_teacher.models.problem import Problem

def get_prompt(agent_input: AgentInput):
    return SYSTEM_PROMPT.format(
        problem_title=agent_input.problem_title,
        problem_description=agent_input.problem_description,
        is_sandbox=agent_input.is_sandbox,
        student_code=agent_input.student_code,
        user_message=agent_input.user_message,
        chat_history=agent_input.chat_history
    )

def get_model(TASK_DIFFICULTY: str):
    return get_groq_model(TASK_DIFFICULTY)

def generate_ai_response(student_session, user_message, problem: Problem, student_code: str):
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
    response = brain.invoke(
        prompt=prompt, 
        config=config
    ).content
    
    return response