from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.student import (
    Student,
    StudentCreate,
    StudentUpdate,
)
from gpt_teacher_db.gpt_teacher.models.classroom import Classroom
from gpt_teacher_db.gpt_teacher.models.classroom_student import ClassroomStudent
from app.utils.security import get_password_hash


def create_student(session: Session, student_in: StudentCreate) -> Student:
    """Cria um novo aluno"""
    student = Student(
        email=student_in.email,
        name=student_in.name,
        hashed_password=get_password_hash(student_in.password),
        is_active=True,
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def get_student_by_id(session: Session, student_id: str) -> Student | None:
    """Busca aluno por ID"""
    return session.get(Student, student_id)


def get_student_by_email(session: Session, email: str) -> Student | None:
    """Busca aluno por email"""
    statement = select(Student).where(Student.email == email)
    return session.exec(statement).first()


def update_student(
    session: Session, student: Student, student_in: StudentUpdate
) -> Student:
    """Atualiza dados do aluno"""
    update_data = student_in.model_dump(exclude_unset=True)

    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    for key, value in update_data.items():
        setattr(student, key, value)

    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def get_student_classrooms(session: Session, student_id: str) -> list[Classroom]:
    """Lista todas as turmas do aluno"""
    statement = (
        select(Classroom)
        .join(ClassroomStudent)
        .where(ClassroomStudent.student_id == student_id)
    )
    return list(session.exec(statement).all())
