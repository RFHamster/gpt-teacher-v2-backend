from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.teacher import (
    Teacher,
    TeacherCreate,
    TeacherUpdate,
)
from app.utils.security import get_password_hash


def create_teacher(session: Session, teacher_in: TeacherCreate) -> Teacher:
    """Cria um novo professor"""
    teacher = Teacher(
        email=teacher_in.email,
        name=teacher_in.name,
        hashed_password=get_password_hash(teacher_in.password),
        is_active=True,
    )
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher


def get_teacher_by_id(session: Session, teacher_id: str) -> Teacher | None:
    """Busca professor por ID"""
    return session.get(Teacher, teacher_id)


def get_teacher_by_email(session: Session, email: str) -> Teacher | None:
    """Busca professor por email"""
    statement = select(Teacher).where(Teacher.email == email)
    return session.exec(statement).first()


def update_teacher(
    session: Session, teacher: Teacher, teacher_in: TeacherUpdate
) -> Teacher:
    """Atualiza dados do professor"""
    update_data = teacher_in.model_dump(exclude_unset=True)

    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    for key, value in update_data.items():
        setattr(teacher, key, value)

    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher
