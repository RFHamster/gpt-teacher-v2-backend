from uuid import UUID

from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.exercise_list import (
    ExerciseList,
    ExerciseListCreate,
    ExerciseListUpdate,
)


def get_lists_by_classroom(session: Session, classroom_id: str) -> list[ExerciseList]:
    return session.exec(
        select(ExerciseList)
        .where(ExerciseList.classroom_id == UUID(classroom_id))
        .order_by(ExerciseList.created_at)
    ).all()


def get_list_by_id(session: Session, list_id: str) -> ExerciseList | None:
    return session.get(ExerciseList, UUID(list_id))


def create_list(
    session: Session,
    classroom_id: str,
    data: ExerciseListCreate,
) -> ExerciseList:
    obj = ExerciseList(
        classroom_id=UUID(classroom_id),
        name=data.name,
        description=data.description,
        deadline=data.deadline,
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def update_list(
    session: Session,
    obj: ExerciseList,
    data: ExerciseListUpdate,
) -> ExerciseList:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def delete_list(session: Session, obj: ExerciseList) -> None:
    session.delete(obj)
    session.commit()
