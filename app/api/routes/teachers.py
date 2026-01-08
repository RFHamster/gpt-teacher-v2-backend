from fastapi import APIRouter

from gpt_teacher_db.gpt_teacher.models.teacher import (
    Teacher,
    TeacherPublic,
    TeacherUpdate,
)

from app.api.deps import SessionDep, CurrentTeacherUser
from app.cruds import teacher as teacher_crud


router = APIRouter(tags=["teachers"])


@router.get("/me", response_model=TeacherPublic)
def get_teacher_me(
    current_user: CurrentTeacherUser,
) -> Teacher:
    """
    Retorna perfil do professor logado
    """
    return current_user


@router.put("/me", response_model=TeacherPublic)
def update_teacher_me(
    session: SessionDep,
    current_user: CurrentTeacherUser,
    teacher_in: TeacherUpdate,
) -> Teacher:
    """
    Atualiza perfil do professor
    """
    teacher = teacher_crud.update_teacher(session, current_user, teacher_in)
    return teacher
