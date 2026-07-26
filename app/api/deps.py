from typing import Annotated, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from gpt_teacher_db.gpt_teacher.models.teacher import Teacher
from gpt_teacher_db.gpt_teacher.models.student import Student

from app.core.config import settings
from app.core.db import get_db
from app.utils.security import decode_jwt_token

reusable_oauth2 = OAuth2PasswordBearer(
	tokenUrl=f'{settings.API_V1_STR}/auth/login/access-token'
)

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_teacher_user(session: SessionDep, token: TokenDep) -> Teacher:
	try:
		token_data = decode_jwt_token(token, verify_exp=True)
	except (InvalidTokenError, ValidationError):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Could not validate credentials',
		)
	user = session.get(Teacher, token_data.sub)

	if not user:
		raise HTTPException(
			status_code=404, detail='Token not related to a Teacher'
		)
	# TODO: reativar quando o campo is_active existir no model Teacher
	# if not user.is_active:
	#     raise HTTPException(status_code=400, detail='Inactive user')
	return user


def get_current_student_user(session: SessionDep, token: TokenDep) -> Student:
	try:
		token_data = decode_jwt_token(token, verify_exp=True)
	except (InvalidTokenError, ValidationError):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Could not validate credentials',
		)
	user = session.get(Student, token_data.sub)

	if not user:
		raise HTTPException(
			status_code=404, detail='Token not related to a Student'
		)
	# TODO: reativar quando o campo is_active existir no model Student
	# if not user.is_active:
	#     raise HTTPException(status_code=400, detail='Inactive user')
	return user


def get_current_teacher_or_student_user(
	session: SessionDep, token: TokenDep
) -> Union[Teacher, Student]:
	"""
	Autentica o token e retorna Teacher ou Student, o que existir.
	Usado em rotas acessíveis por ambos os tipos de usuário.
	"""
	try:
		token_data = decode_jwt_token(token, verify_exp=True)
	except (InvalidTokenError, ValidationError):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Could not validate credentials',
		)

	user = session.get(Teacher, token_data.sub)
	if user:
		return user

	user = session.get(Student, token_data.sub)
	if user:
		return user

	raise HTTPException(
		status_code=404, detail='Token not related to a valid user'
	)


CurrentTeacherUser = Annotated[Teacher, Depends(get_current_teacher_user)]
CurrentStudentUser = Annotated[Student, Depends(get_current_student_user)]
CurrentTeacherOrStudentUser = Annotated[
	Union[Teacher, Student], Depends(get_current_teacher_or_student_user)
]