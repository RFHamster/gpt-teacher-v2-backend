from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from gpt_teacher_db.gpt_teacher.models.teacher import (
    Teacher,
    TeacherCreate,
    TeacherPublic,
)
from gpt_teacher_db.gpt_teacher.models.student import (
    Student,
    StudentCreate,
    StudentPublic,
)

from app.api.deps import SessionDep
from app.core.config import settings
from app.cruds import teacher as teacher_crud
from app.cruds import student as student_crud
from app.utils import auth, security


router = APIRouter(tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserType:
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


@router.post("/register/teacher", response_model=TeacherPublic)
def register_teacher(
    session: SessionDep,
    teacher_in: TeacherCreate,
) -> Teacher:
    """
    Cadastro de professor
    """
    # Verifica se o email já existe
    existing_teacher = teacher_crud.get_teacher_by_email(session, teacher_in.email)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Email already registered")

    teacher = teacher_crud.create_teacher(session, teacher_in)
    return teacher


@router.post("/register/student", response_model=StudentPublic)
def register_student(
    session: SessionDep,
    student_in: StudentCreate,
) -> Student:
    """
    Cadastro de aluno
    """
    # Verifica se o email já existe
    existing_student = student_crud.get_student_by_email(session, student_in.email)
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")

    student = student_crud.create_student(session, student_in)
    return student


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Use client_id to specify user type: 'teacher' or 'student'
    """
    if form_data.client_id == UserType.TEACHER:
        user = auth.authenticate_teacher(
            session=session,
            username=form_data.username,
            password=form_data.password,
        )
    elif form_data.client_id == UserType.STUDENT:
        user = auth.authenticate_student(
            session=session,
            username=form_data.username,
            password=form_data.password,
        )
    else:
        raise HTTPException(
            status_code=400, detail="Invalid client_id. Use 'teacher' or 'student'"
        )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    # TODO ADD THIS ON MODEL
    # elif not user.is_active:
    #     raise HTTPException(status_code=403, detail="Inactive user")

    access_token = security.create_access_token(
        str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token)
