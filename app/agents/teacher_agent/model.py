from pydantic import BaseModel

from gpt_teacher_db.gpt_teacher.enum import TeachingMethodology


class AgentInput(BaseModel):
	problem_title: str
	session_id: str  ## RENAME THIS
	problem_description: str
	problem_category: str | None = None
	student_code: str
	user_message: str
	methodology: TeachingMethodology = TeachingMethodology.SOCRATIC