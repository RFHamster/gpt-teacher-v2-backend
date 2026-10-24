from fastapi import APIRouter, HTTPException

from gpt_teacher_db.gpt_teacher.models.exercise_list import (
    ExerciseList,
    ExerciseListCreate,
    ExerciseListPublic,
    ExerciseListUpdate,
)

from app.api.deps import SessionDep, CurrentTeacherUser, CurrentTeacherOrStudentUser
from gpt_teacher_db.gpt_teacher.models.student import Student
from app.cruds import classroom as classroom_crud
from app.cruds import exercise_list as list_crud

router = APIRouter(tags=['lists'])


def _assert_teacher_owns_classroom(session, classroom_id: str, teacher_id):
    classroom = classroom_crud.get_classroom_by_id(session, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail='Classroom not found')
    if classroom.teacher_id != teacher_id:
        raise HTTPException(status_code=403, detail='Not authorized')
    return classroom


@router.get('/classrooms/{classroom_id}/lists', response_model=list[ExerciseListPublic])
def get_lists(
    session: SessionDep,
    current_user: CurrentTeacherOrStudentUser,
    classroom_id: str,
):
    classroom = classroom_crud.get_classroom_by_id(session, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail='Classroom not found')

    if isinstance(current_user, Student):
        from app.cruds.classroom import is_student_in_classroom
        if not is_student_in_classroom(session, classroom_id, current_user.id):
            raise HTTPException(status_code=403, detail='Not authorized')
    else:
        if classroom.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail='Not authorized')

    return list_crud.get_lists_by_classroom(session, classroom_id)


@router.post('/classrooms/{classroom_id}/lists', response_model=ExerciseListPublic)
def create_list(
    session: SessionDep,
    current_user: CurrentTeacherUser,
    classroom_id: str,
    data: ExerciseListCreate,
) -> ExerciseList:
    _assert_teacher_owns_classroom(session, classroom_id, current_user.id)
    return list_crud.create_list(session, classroom_id, data)


@router.get('/lists/{list_id}', response_model=ExerciseListPublic)
def get_list(
    session: SessionDep,
    current_user: CurrentTeacherUser,
    list_id: str,
) -> ExerciseList:
    obj = list_crud.get_list_by_id(session, list_id)
    if not obj:
        raise HTTPException(status_code=404, detail='List not found')
    _assert_teacher_owns_classroom(session, str(obj.classroom_id), current_user.id)
    return obj


@router.put('/lists/{list_id}', response_model=ExerciseListPublic)
def update_list(
    session: SessionDep,
    current_user: CurrentTeacherUser,
    list_id: str,
    data: ExerciseListUpdate,
) -> ExerciseList:
    obj = list_crud.get_list_by_id(session, list_id)
    if not obj:
        raise HTTPException(status_code=404, detail='List not found')
    _assert_teacher_owns_classroom(session, str(obj.classroom_id), current_user.id)
    return list_crud.update_list(session, obj, data)


@router.delete('/lists/{list_id}')
def delete_list(
    session: SessionDep,
    current_user: CurrentTeacherUser,
    list_id: str,
):
    obj = list_crud.get_list_by_id(session, list_id)
    if not obj:
        raise HTTPException(status_code=404, detail='List not found')
    _assert_teacher_owns_classroom(session, str(obj.classroom_id), current_user.id)
    list_crud.delete_list(session, obj)
    return {'message': 'List deleted'}
