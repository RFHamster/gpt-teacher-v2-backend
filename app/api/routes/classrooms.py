from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from gpt_teacher_db.gpt_teacher.models.classroom import (
	Classroom,
	ClassroomCreate,
	ClassroomUpdate,
	ClassroomPublic,
)
from gpt_teacher_db.gpt_teacher.models.student import StudentPublic

from app.api.deps import SessionDep, CurrentTeacherUser, CurrentStudentUser
from app.schemas.classroom_student import StudentMethodologyUpdateRequest
from app.cruds import classroom as classroom_crud
from app.cruds import student as student_crud


router = APIRouter(tags=['classrooms'])


class AddStudentRequest(BaseModel):
	student_id: str


@router.post('', response_model=ClassroomPublic)
def create_classroom(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	classroom_in: ClassroomCreate,
) -> Classroom:
	"""
	Cria nova turma
	"""
	classroom = classroom_crud.create_classroom(
		session, classroom_in, current_user.id
	)
	return classroom


@router.get('', response_model=list[ClassroomPublic])
def get_classrooms(
	session: SessionDep,
	current_user: CurrentTeacherUser,
):
	"""
	Lista turmas do professor
	"""
	classrooms = classroom_crud.get_classrooms_by_teacher(
		session, current_user.id
	)
	return classrooms


@router.get('/{id}', response_model=ClassroomPublic)
def get_classroom(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
) -> Classroom:
	"""
	Detalhes de uma turma
	"""
	classroom = classroom_crud.get_classroom_by_id(session, id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to access this classroom'
		)

	return classroom


@router.put('/{id}', response_model=ClassroomPublic)
def update_classroom(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
	classroom_in: ClassroomUpdate,
) -> Classroom:
	"""
	Atualiza turma
	"""
	classroom = classroom_crud.get_classroom_by_id(session, id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to update this classroom'
		)

	classroom = classroom_crud.update_classroom(
		session, classroom, classroom_in
	)
	return classroom


@router.delete('/{id}')
def delete_classroom(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
):
	"""
	Remove turma
	"""
	classroom = classroom_crud.get_classroom_by_id(session, id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to delete this classroom'
		)

	classroom_crud.delete_classroom(session, classroom)
	return {'message': 'Classroom deleted successfully'}


@router.post('/{id}/students')
def add_student_to_classroom(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
	request: AddStudentRequest,
):
	"""
	Adiciona aluno à turma
	"""
	classroom = classroom_crud.get_classroom_by_id(session, id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to modify this classroom'
		)

	student = student_crud.get_student_by_id(session, request.student_id)
	if not student:
		raise HTTPException(status_code=404, detail='Student not found')

	if classroom_crud.is_student_in_classroom(session, id, request.student_id):
		raise HTTPException(
			status_code=400, detail='Student already in classroom'
		)

	classroom_crud.add_student_to_classroom(session, id, request.student_id)
	return {'message': 'Student added successfully'}


@router.delete('/{id}/students/{student_id}')
def remove_student_from_classroom(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
	student_id: str,
):
	"""
	Remove aluno da turma
	"""
	classroom = classroom_crud.get_classroom_by_id(session, id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to modify this classroom'
		)

	classroom_crud.remove_student_from_classroom(session, id, student_id)
	return {'message': 'Student removed successfully'}


@router.get('/{id}/students', response_model=list[StudentPublic])
def get_classroom_students(
	session: SessionDep,
	current_user: CurrentTeacherUser,
	id: str,
):
	"""
	Lista alunos da turma
	"""
	classroom = classroom_crud.get_classroom_by_id(session, id)
	if not classroom:
		raise HTTPException(status_code=404, detail='Classroom not found')

	if classroom.teacher_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to access this classroom'
		)

	students = classroom_crud.get_classroom_students(session, id)
	return students


@router.put('/{classroom_id}/students/me/methodology')
def update_my_methodology(
	session: SessionDep,
	current_user: CurrentStudentUser,
	classroom_id: str,
	request: StudentMethodologyUpdateRequest,
):
	"""
	Aluno atualiza sua própria metodologia dentro desta turma.
	"""
	classroom_student = classroom_crud.get_classroom_student(
		session, classroom_id, current_user.id
	)
	if not classroom_student:
		raise HTTPException(
			status_code=404, detail='Matrícula não encontrada nesta turma'
		)

	classroom_crud.update_classroom_student_methodology(
		session, classroom_student, request.methodology
	)
	return {'message': 'Metodologia atualizada com sucesso'}