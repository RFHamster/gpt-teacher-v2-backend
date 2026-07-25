from uuid import UUID
from sqlmodel import SQLModel


class StudentSessionCreateRequest(SQLModel):
	"""Corpo esperado da API para criar sessão.

	Não inclui student_id: esse valor vem do usuário autenticado
	(current_user), não do que o cliente manda no body.
	"""

	problem_id: UUID