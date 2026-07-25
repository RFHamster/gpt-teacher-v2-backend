from datetime import datetime

from gpt_teacher_db.gpt_teacher.models.chat_message import ChatMessagePublic


class ChatMessagePublicWithTimestamp(ChatMessagePublic):
	"""Estende o schema oficial só para expor created_at na resposta da API.

	Não altera o pacote gpt_teacher_db - o dado já existe no banco
	(BaseModelGPTTeacher_), só não estava sendo retornado pela API.
	"""

	created_at: datetime