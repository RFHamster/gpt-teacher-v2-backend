from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.student_session import (
	StudentSession,
	StudentSessionCreate,
)
from gpt_teacher_db.gpt_teacher.enum import SessionStatus
from gpt_teacher_db.core import current_datetime


def create_student_session(
	session: Session, session_in: StudentSessionCreate
) -> StudentSession:
	"""Cria uma nova sessão do aluno"""
	# Fecha qualquer sessão aberta anterior do aluno
	close_active_sessions(session, str(session_in.student_id))

	student_session = StudentSession(
		student_id=session_in.student_id,
		problem_id=session_in.problem_id,
		status=SessionStatus.OPEN,
	)
	session.add(student_session)
	session.commit()
	session.refresh(student_session)
	return student_session


def get_student_session_by_id(
	session: Session, session_id: str
) -> StudentSession | None:
	"""Busca sessão por ID"""
	return session.get(StudentSession, session_id)


def get_active_session_by_student(
	session: Session, student_id: str
) -> StudentSession | None:
	"""Busca a sessão aberta do aluno"""
	statement = select(StudentSession).where(
		StudentSession.student_id == student_id,
		StudentSession.status == SessionStatus.OPEN,
	)
	return session.exec(statement).first()


def close_session(
	session: Session, student_session: StudentSession
) -> StudentSession:
	"""Fecha uma sessão"""
	student_session.status = SessionStatus.CLOSED
	student_session.closed_at = current_datetime()
	session.add(student_session)
	session.commit()
	session.refresh(student_session)
	return student_session


def close_active_sessions(session: Session, student_id: str) -> None:
	"""Fecha todas as sessões abertas do aluno"""
	statement = select(StudentSession).where(
		StudentSession.student_id == student_id,
		StudentSession.status == SessionStatus.OPEN,
	)
	active_sessions = session.exec(statement).all()

	for active_session in active_sessions:
		active_session.status = SessionStatus.CLOSED
		active_session.closed_at = current_datetime()
		session.add(active_session)

	session.commit()


def get_sessions_by_problem_and_student(
	session: Session, problem_id: str, student_id: str
) -> list[StudentSession]:
	"""Lista todas as sessões de um aluno em um problema"""
	statement = (
		select(StudentSession)
		.where(
			StudentSession.problem_id == problem_id,
			StudentSession.student_id == student_id,
		)
		.order_by(StudentSession.created_at.desc())
	)

	return list(session.exec(statement).all())