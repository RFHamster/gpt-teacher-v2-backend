from gpt_teacher_db.gpt_teacher.enum import TeachingMethodology
from sqlmodel import SQLModel


class StudentMethodologyUpdateRequest(SQLModel):
	"""Corpo esperado para o aluno atualizar sua própria metodologia
	dentro de uma turma específica."""

	methodology: TeachingMethodology