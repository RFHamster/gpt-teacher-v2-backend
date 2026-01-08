from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.problem import (
    Problem,
    ProblemCreate,
    ProblemUpdate,
)


def create_problem(
    session: Session,
    problem_in: ProblemCreate,
    classroom_id: str,
    created_by_student_id: str | None = None,
) -> Problem:
    """Cria um novo problema"""
    problem = Problem(
        title=problem_in.title,
        description=problem_in.description,
        file_url=problem_in.file_url,
        classroom_id=classroom_id,
        is_sandbox=problem_in.is_sandbox
        if hasattr(problem_in, "is_sandbox")
        else False,
        created_by_student_id=created_by_student_id,
    )
    session.add(problem)
    session.commit()
    session.refresh(problem)
    return problem


def get_problem_by_id(session: Session, problem_id: str) -> Problem | None:
    """Busca problema por ID"""
    return session.get(Problem, problem_id)


def get_problems_by_classroom(
    session: Session, classroom_id: str, include_sandbox: bool = False
) -> list[Problem]:
    """Lista todos os problemas de uma turma"""
    statement = select(Problem).where(Problem.classroom_id == classroom_id)

    if not include_sandbox:
        statement = statement.where(Problem.is_sandbox == False)

    return list(session.exec(statement).all())


def get_sandbox_problems_by_classroom(
    session: Session, classroom_id: str
) -> list[Problem]:
    """Lista problemas sandbox de uma turma"""
    statement = select(Problem).where(
        Problem.classroom_id == classroom_id, Problem.is_sandbox == True
    )
    return list(session.exec(statement).all())


def update_problem(
    session: Session, problem: Problem, problem_in: ProblemUpdate
) -> Problem:
    """Atualiza dados do problema"""
    update_data = problem_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(problem, key, value)

    session.add(problem)
    session.commit()
    session.refresh(problem)
    return problem


def delete_problem(session: Session, problem: Problem) -> None:
    """Remove um problema"""
    session.delete(problem)
    session.commit()
