from fastapi import APIRouter, HTTPException

from gpt_teacher_db.gpt_teacher.models.student_session import (
	StudentSession,
	StudentSessionCreate,
	StudentSessionPublic,
)

from app.api.deps import SessionDep, CurrentStudentUser
from app.schemas.student_session import StudentSessionCreateRequest
from app.cruds import student_session as session_crud
from app.cruds import problem as problem_crud
from app.cruds import classroom as classroom_crud


router = APIRouter(tags=['student-sessions'])


@router.post('', response_model=StudentSessionPublic)
def create_student_session(
	session: SessionDep,
	current_user: CurrentStudentUser,
	session_in: StudentSessionCreateRequest,
) -> StudentSession:
	"""
	Inicia sessão (fecha anterior automaticamente)
	"""
	# Verifica se o problema existe
	problem = problem_crud.get_problem_by_id(session, session_in.problem_id)
	if not problem:
		raise HTTPException(status_code=404, detail='Problem not found')

	# Verifica se o aluno tem acesso ao problema (está na turma)
	if not classroom_crud.is_student_in_classroom(
		session, problem.classroom_id, str(current_user.id)
	):
		raise HTTPException(
			status_code=403, detail='Not authorized to access this problem'
		)

	# Monta o objeto completo que o model do banco espera,
	# preenchendo student_id a partir do usuário autenticado
	full_session_data = StudentSessionCreate(
		student_id=current_user.id,
		problem_id=session_in.problem_id,
	)

	student_session = session_crud.create_student_session(
		session, full_session_data
	)
	return student_session


@router.get('/active', response_model=StudentSessionPublic | None)
def get_active_session(
	session: SessionDep,
	current_user: CurrentStudentUser,
):
	"""
	Retorna sessão ativa do aluno
	"""
	active_session = session_crud.get_active_session_by_student(
		session, str(current_user.id)
	)
	return active_session


@router.get('/{id}', response_model=StudentSessionPublic)
def get_student_session(
	session: SessionDep,
	current_user: CurrentStudentUser,
	id: str,
) -> StudentSession:
	"""
	Detalhes da sessão (inclui messages via relationship)
	"""
	student_session = session_crud.get_student_session_by_id(session, id)
	if not student_session:
		raise HTTPException(status_code=404, detail='Session not found')

	if student_session.student_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to access this session'
		)

	return student_session


@router.post('/{id}/close', response_model=StudentSessionPublic)
def close_student_session(
	session: SessionDep,
	current_user: CurrentStudentUser,
	id: str,
) -> StudentSession:
	"""
	Fecha sessão manualmente
	"""
	student_session = session_crud.get_student_session_by_id(session, id)
	if not student_session:
		raise HTTPException(status_code=404, detail='Session not found')

	if student_session.student_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to close this session'
		)

	if student_session.status.value != 'open':
		raise HTTPException(
			status_code=400, detail='Session is already closed'
		)

	student_session = session_crud.close_session(session, student_session)
	return student_session


@router.get(
	'/problems/{problem_id}/sessions',
	response_model=list[StudentSessionPublic],
)
def get_problem_student_sessions(
	session: SessionDep,
	current_user: CurrentStudentUser,
	problem_id: str,
):
	"""
	Histórico de sessões do aluno no problema
	"""
	problem = problem_crud.get_problem_by_id(session, problem_id)
	if not problem:
		raise HTTPException(status_code=404, detail='Problem not found')

	if not classroom_crud.is_student_in_classroom(
		session, problem.classroom_id, str(current_user.id)
	):
		raise HTTPException(
			status_code=403, detail='Not authorized to access this problem'
		)

	sessions = session_crud.get_sessions_by_problem_and_student(
		session, problem_id, str(current_user.id)
	)
	return sessions