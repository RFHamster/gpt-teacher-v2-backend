from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.classroom import (
    Classroom,
    ClassroomCreate,
    ClassroomUpdate,
)
from gpt_teacher_db.gpt_teacher.models.classroom_student import ClassroomStudent
from gpt_teacher_db.gpt_teacher.models.student import Student


def create_classroom(
    session: Session, classroom_in: ClassroomCreate, teacher_id: str
) -> Classroom:
    """Cria uma nova turma"""
    classroom = Classroom(
        name=classroom_in.name,
        description=classroom_in.description,
        teacher_id=teacher_id,
    )
    session.add(classroom)
    session.commit()
    session.refresh(classroom)
    return classroom


def get_classroom_by_id(session: Session, classroom_id: str) -> Classroom | None:
    """Busca turma por ID"""
    return session.get(Classroom, classroom_id)


def get_classrooms_by_teacher(session: Session, teacher_id: str) -> list[Classroom]:
    """Lista todas as turmas de um professor"""
    statement = select(Classroom).where(Classroom.teacher_id == teacher_id)
    return list(session.exec(statement).all())


def update_classroom(
    session: Session, classroom: Classroom, classroom_in: ClassroomUpdate
) -> Classroom:
    """Atualiza dados da turma"""
    update_data = classroom_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(classroom, key, value)

    session.add(classroom)
    session.commit()
    session.refresh(classroom)
    return classroom


def delete_classroom(session: Session, classroom: Classroom) -> None:
    """Remove uma turma"""
    session.delete(classroom)
    session.commit()


def add_student_to_classroom(
    session: Session, classroom_id: str, student_id: str
) -> ClassroomStudent:
    """Adiciona um aluno à turma"""
    classroom_student = ClassroomStudent(
        classroom_id=classroom_id,
        student_id=student_id,
    )
    session.add(classroom_student)
    session.commit()
    session.refresh(classroom_student)
    return classroom_student


def remove_student_from_classroom(
    session: Session, classroom_id: str, student_id: str
) -> None:
    """Remove um aluno da turma"""
    statement = select(ClassroomStudent).where(
        ClassroomStudent.classroom_id == classroom_id,
        ClassroomStudent.student_id == student_id,
    )
    classroom_student = session.exec(statement).first()
    if classroom_student:
        session.delete(classroom_student)
        session.commit()


def get_classroom_students(session: Session, classroom_id: str) -> list[Student]:
    """Lista todos os alunos de uma turma"""
    statement = (
        select(Student)
        .join(ClassroomStudent)
        .where(ClassroomStudent.classroom_id == classroom_id)
    )
    return list(session.exec(statement).all())


def is_student_in_classroom(
    session: Session, classroom_id: str, student_id: str
) -> bool:
    """Verifica se o aluno está na turma"""
    statement = select(ClassroomStudent).where(
        ClassroomStudent.classroom_id == classroom_id,
        ClassroomStudent.student_id == student_id,
    )
    return session.exec(statement).first() is not None
