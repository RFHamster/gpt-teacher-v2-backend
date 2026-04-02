from pydantic import BaseModel


class AgentInput(BaseModel):
    problem_title: str
    problem_description: str
    is_sandbox: bool
    student_code: str
    user_message: str
    session_id: str
    student_id: str



