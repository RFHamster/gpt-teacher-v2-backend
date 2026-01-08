from datetime import datetime
from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.student_session import (
    StudentSession,
    StudentSessionCreate,
)


def create_student_session(
    session: Session, session_in: StudentSessionCreate, student_id: str
) -> StudentSession:
    """Cria uma nova sessão do aluno"""
    # Fecha qualquer sessão ativa anterior do aluno
    close_active_sessions(session, student_id)

    student_session = StudentSession(
        student_id=student_id,
        problem_id=session_in.problem_id,
        is_active=True,
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
    """Busca a sessão ativa do aluno"""
    statement = select(StudentSession).where(
        StudentSession.student_id == student_id, StudentSession.is_active == True
    )
    return session.exec(statement).first()


def close_session(session: Session, student_session: StudentSession) -> StudentSession:
    """Fecha uma sessão"""
    student_session.is_active = False
    student_session.ended_at = datetime.utcnow()
    session.add(student_session)
    session.commit()
    session.refresh(student_session)
    return student_session


def close_active_sessions(session: Session, student_id: str) -> None:
    """Fecha todas as sessões ativas do aluno"""
    statement = select(StudentSession).where(
        StudentSession.student_id == student_id, StudentSession.is_active == True
    )
    active_sessions = session.exec(statement).all()

    for active_session in active_sessions:
        active_session.is_active = False
        active_session.ended_at = datetime.utcnow()
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
