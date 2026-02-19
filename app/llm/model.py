from agents import get_llm
from gpt_teacher_db.gpt_teacher.models.problem import Problem

def generate_ai_response(student_session: str, user_message: str, problem: Problem, student_code: str) -> str:
    brain = get_llm()

    full_input = {
        "problem_title": problem.title,
        "problem_description": problem.description or "Sem descrição.",
        "is_sandbox": "Sim" if problem.is_sandbox else "Não",
        "student_code": student_code,
        "user_message": user_message 
    }

    return brain.invoke(
        full_input,
        config={"configurable": {"session_id": student_session}}
    ).content
    