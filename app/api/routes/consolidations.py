from fastapi import APIRouter, HTTPException

from gpt_teacher_db.gpt_teacher.models.consolidated import ConsolidatedPublic

from app.api.deps import SessionDep, CurrentTeacherUser
from app.cruds import consolidated as consolidated_crud
from app.cruds import student as student_crud
from app.cruds import problem as problem_crud
from app.cruds import classroom as classroom_crud


router = APIRouter(tags=["consolidations"])


@router.get(
    "/students/{student_id}/consolidations", response_model=list[ConsolidatedPublic]
)
def get_student_consolidations(
    session: SessionDep,
    current_user: CurrentTeacherUser,
    student_id: str,
):
    """
    Consolidações de um aluno específico
    """
    # Verifica se o aluno existe
    student = student_crud.get_student_by_id(session, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # TODO: Verificar se o professor tem acesso a esse aluno
    # (o aluno está em alguma turma do professor)

    consolidations = consolidated_crud.get_consolidations_by_student(
        session, student_id
    )
    return consolidations


@router.get(
    "/problems/{problem_id}/consolidations", response_model=list[ConsolidatedPublic]
)
def get_problem_consolidations(
    session: SessionDep,
    current_user: CurrentTeacherUser,
    problem_id: str,
):
    """
    Consolidações de um problema
    """
    # Verifica se o problema existe
    problem = problem_crud.get_problem_by_id(session, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Verifica se o professor é dono da turma
    classroom = classroom_crud.get_classroom_by_id(session, problem.classroom_id)
    if not classroom or classroom.teacher_id != str(current_user.id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this problem"
        )

    consolidations = consolidated_crud.get_consolidations_by_problem(
        session, problem_id
    )
    return consolidations
