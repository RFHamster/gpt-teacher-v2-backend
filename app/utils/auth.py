from sqlmodel import Session, or_, select

from gpt_teacher_db.gpt_teacher.models.teacher import Teacher
from gpt_teacher_db.gpt_teacher.models.student import Student

from app.utils.security import verify_password


def authenticate_teacher(
    session: Session, username: str, password: str
) -> Teacher | None:
    """
    Autentica um professor com username (email) e senha.
    """
    statement = select(Teacher).where(Teacher.email == username)
    teacher = session.exec(statement).first()

    if not teacher:
        return None
    if not verify_password(password, teacher.hashed_password):
        return None
    return teacher


def authenticate_student(
    session: Session, username: str, password: str
) -> Student | None:
    """
    Autentica um aluno com username (email) e senha.
    """
    statement = select(Student).where(
        or_(
            Student.email == username, 
            Student.registration_number == username
        )
    )
    student = session.exec(statement).first()

    if not student:
        return None
    if not verify_password(password, student.hashed_password):
        return None
    return student
