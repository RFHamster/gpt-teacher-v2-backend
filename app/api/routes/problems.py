from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from gpt_teacher_db.gpt_teacher.models.problem import (
	Problem,
	ProblemCreate,
	ProblemUpdate,
	ProblemPublic,
)
from gpt_teacher_db.gpt_teacher.models.teacher import Teacher
from gpt_teacher_db.gpt_teacher.models.student import Student

from app.api.deps import SessionDep, CurrentTeacherUser, CurrentStudentUser
from app.cruds import classroom as classroom_crud
from app.cruds import problem as problem_crud


router = APIRouter(tags=['problems'])


class ProblemSuggestRequest(BaseModel):
	file_url: str


class ProblemSuggestResponse(BaseModel):
	title: str
	description: str


@router.post(
	'/classrooms/{classroom_id}/problems', response_model=ProblemPublic
)
async def create_problem(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	classroom_id: str,
	title: Annotated[str, Form()],
	description: Annotated[str, Form()],
	category: Annotated[str | None, Form()] = None,
	file: UploadFile = File(None),
) -> Problem:
	"""
	Cria problema na turma (FormData com arquivo opcional)
	"""
	classroom = classroom_crud.get_classroom_by_id(session, classroom_id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403,
			detail='Not authorized to add problems to this classroom',
		)

	file_path = None
	if file:
		file_path = f'uploads/{file.filename}'

	problem_in = ProblemCreate(
		title=title,
		description=description,
		category=category,
		classroom_id=classroom_id,
	)

	problem = problem_crud.create_problem(
		session, problem_in, classroom_id, file_path=file_path
	)
	return problem


@router.get(
	'/classrooms/{classroom_id}/problems', response_model=list[ProblemPublic]
)
def get_classroom_problems(
	session: SessionDep,
	current_user: Union[Teacher, Student],
	classroom_id: str,
):
	"""
	Lista problemas da turma (acessível por teacher e student)
	"""
	classroom = classroom_crud.get_classroom_by_id(session, classroom_id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if isinstance(current_user, Teacher):
		if classroom.teacher_id != current_user.id:
			raise HTTPException(
				status_code=403,
				detail='Not authorized to access this classroom',
			)
	elif isinstance(current_user, Student):
		if not classroom_crud.is_student_in_classroom(
			session, classroom_id, current_user.id
		):
			raise HTTPException(
				status_code=403,
				detail='Not authorized to access this classroom',
			)

	problems = problem_crud.get_problems_by_classroom(
		session, classroom_id, include_sandbox=False
	)
	return problems


@router.get('/problems/{id}', response_model=ProblemPublic)
def get_problem(
	session: SessionDep,
	current_user: Union[Teacher, Student],
	id: str,
) -> Problem:
	"""
	Detalhes de um problema
	"""
	problem = problem_crud.get_problem_by_id(session, id)
	if not problem:
		raise HTTPException(status_code=404, detail='Problem not found')

	classroom = classroom_crud.get_classroom_by_id(
		session, problem.classroom_id
	)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if isinstance(current_user, Teacher):
		if classroom.teacher_id != current_user.id:
			raise HTTPException(
				status_code=403, detail='Not authorized to access this problem'
			)
	elif isinstance(current_user, Student):
		if not classroom_crud.is_student_in_classroom(
			session, problem.classroom_id, current_user.id
		):
			raise HTTPException(
				status_code=403, detail='Not authorized to access this problem'
			)

	return problem


@router.put('/problems/{id}', response_model=ProblemPublic)
def update_problem(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
	problem_in: ProblemUpdate,
) -> Problem:
	"""
	Atualiza problema
	"""
	problem = problem_crud.get_problem_by_id(session, id)
	if not problem:
		raise HTTPException(status_code=404, detail='Problem not found')

	classroom = classroom_crud.get_classroom_by_id(
		session, problem.classroom_id
	)
	if not classroom or classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to update this problem'
		)

	problem = problem_crud.update_problem(session, problem, problem_in)
	return problem


@router.delete('/problems/{id}')
def delete_problem(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
):
	"""
	Remove problema
	"""
	problem = problem_crud.get_problem_by_id(session, id)
	if not problem:
		raise HTTPException(status_code=404, detail='Problem not found')

	classroom = classroom_crud.get_classroom_by_id(
		session, problem.classroom_id
	)
	if not classroom or classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to delete this problem'
		)

	problem_crud.delete_problem(session, problem)
	return {'message': 'Problem deleted successfully'}


@router.post('/problems/sandbox', response_model=ProblemPublic)
async def create_sandbox_problem(
	session: SessionDep,
	current_user: CurrentStudentUser,
	classroom_id: Annotated[str, Form()],
	title: Annotated[str, Form()],
	description: Annotated[str, Form()],
	category: Annotated[str | None, Form()] = None,
	file: UploadFile = File(None),
) -> Problem:
	"""
	Aluno cria problema sandbox
	"""
	if not classroom_crud.is_student_in_classroom(
		session, classroom_id, current_user.id
	):
		raise HTTPException(
			status_code=403, detail='Not authorized to access this classroom'
		)

	file_path = None
	if file:
		file_path = f'uploads/{file.filename}'

	problem_in = ProblemCreate(
		title=title,
		description=description,
		category=category,
		classroom_id=classroom_id,
	)

	problem = problem_crud.create_problem(
		session,
		problem_in,
		classroom_id,
		file_path=file_path,
		is_sandbox=True,
		created_by_student_id=current_user.id,
	)
	return problem


@router.get(
	'/classrooms/{id}/problems/sandbox', response_model=list[ProblemPublic]
)
def get_sandbox_problems(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
):
	"""
	Lista problemas sandbox da turma
	"""
	classroom = classroom_crud.get_classroom_by_id(session, id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to access this classroom'
		)

	problems = problem_crud.get_sandbox_problems_by_classroom(session, id)
	return problems


@router.post('/problems/suggest', response_model=ProblemSuggestResponse)
def suggest_problem(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	request: ProblemSuggestRequest,
) -> ProblemSuggestResponse:
	"""
	IA sugere título/descrição do problema
	"""
	return ProblemSuggestResponse(
		title='Problema sugerido pela IA',
		description='Descrição sugerida pela IA baseada no arquivo fornecido.',
	)