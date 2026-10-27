from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.consolidated import Consolidated
from gpt_teacher_db.gpt_teacher.models.student_session import StudentSession


def get_consolidations_by_student(
	session: Session, student_id: str
) -> list[Consolidated]:
	"""Lista todas as consolidações de um aluno (via join com StudentSession)"""
	statement = (
		select(Consolidated)
		.join(StudentSession, Consolidated.session_id == StudentSession.id)
		.where(StudentSession.student_id == student_id)
		.order_by(Consolidated.created_at.desc())
	)

	return list(session.exec(statement).all())


def get_consolidations_by_problem(
	session: Session, problem_id: str
) -> list[Consolidated]:
	"""Lista todas as consolidações de um problema"""
	statement = (
		select(Consolidated)
		.where(Consolidated.problem_id == problem_id)
		.order_by(Consolidated.created_at.desc())
	)

	return list(session.exec(statement).all())


def create_consolidated(
	session: Session,
	student_id: str,
	problem_id: str,
	session_id: str,
	content: str,
) -> Consolidated:
	"""Cria uma nova consolidação"""
	consolidated = Consolidated(
		student_id=student_id,
		problem_id=problem_id,
		session_id=session_id,
		content=content,
	)
	session.add(consolidated)
	session.commit()
	session.refresh(consolidated)
	return consolidated
