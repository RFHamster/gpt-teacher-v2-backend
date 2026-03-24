from pydantic import BaseModel


class AgentInput(BaseModel):
	problem_title: str
	session_id: str  ## RENAME THIS
	problem_description: str
	is_sandbox: bool
	student_code: str
	user_message: str
	chat_history: list[dict[str, str]]
