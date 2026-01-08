from fastapi import APIRouter

from gpt_teacher_db.gpt_teacher.models.student import (
    Student,
    StudentPublic,
    StudentUpdate,
)
from gpt_teacher_db.gpt_teacher.models.classroom import ClassroomPublic

from app.api.deps import SessionDep, CurrentStudentUser
from app.cruds import student as student_crud


router = APIRouter(tags=["students"])


@router.get("/me", response_model=StudentPublic)
def get_student_me(
    current_user: CurrentStudentUser,
) -> Student:
    """
    Retorna perfil do aluno logado
    """
    return current_user


@router.put("/me", response_model=StudentPublic)
def update_student_me(
    session: SessionDep,
    current_user: CurrentStudentUser,
    student_in: StudentUpdate,
) -> Student:
    """
    Atualiza perfil do aluno
    """
    student = student_crud.update_student(session, current_user, student_in)
    return student


@router.get("/me/classrooms", response_model=list[ClassroomPublic])
def get_student_classrooms(
    session: SessionDep,
    current_user: CurrentStudentUser,
):
    """
    Lista turmas que o aluno participa
    """
    classrooms = student_crud.get_student_classrooms(session, str(current_user.id))
    return classrooms
