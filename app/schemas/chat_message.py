from datetime import datetime
from typing import Optional

from gpt_teacher_db.gpt_teacher.models.chat_message import ChatMessagePublic


class ChatMessagePublicWithTimestamp(ChatMessagePublic):
	"""Estende o schema oficial só para expor created_at na resposta da API."""

	created_at: datetime


class ChatMessagePublicForTeacher(ChatMessagePublicWithTimestamp):
	"""Versão para professor: omite o código parcial enviado durante o chat.

	O código do aluno visível ao professor é somente o submitted_code da sessão.
	code_review (saída da IA) permanece visível.
	"""

	code: Optional[str] = None