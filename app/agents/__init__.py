from model import get_model
from gpt_teacher_db.gpt_teacher.models.problem import Problem
from prompt import (
    PromptParameters,  
    get_system_prompt
)


def get_prompt(problem_title, problem_description, is_sandbox, student_code, user_message):
    prompt_params = PromptParameters(
        problem_title=problem_title,
        problem_description=problem_description,
        is_sandbox=is_sandbox,
        student_code=student_code,
        user_message=user_message
    )
    return get_system_prompt(prompt_params)


def generate_ai_response(student_session, user_message, problem, student_code):
    brain = get_model(student_code_complexity = "INICIANTE")
    prompt = get_prompt(problem.title, problem.description, problem.is_sandbox, student_code, user_message)
    config = {"configurable": {"session_id": student_session}}


    response = brain.invoke(
        prompt=prompt, 
        config=config
    ).content
    
    return response
    