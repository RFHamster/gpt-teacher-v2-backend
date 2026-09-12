from langchain_groq import ChatGroq

from app.core.config import settings


class GroqModels(str):
	LOW = 'openai/gpt-oss-20b'
	MEDIUM = 'openai/gpt-oss-120b'
	HIGH = 'openai/gpt-oss-120b'


MODEL_BY_DIFICULTY = {
	'LOW': GroqModels.LOW,
	'MEDIUM': GroqModels.MEDIUM,
	'HIGH': GroqModels.HIGH,
}


def get_model_by_difficulty(task_dificulty: str) -> ChatGroq:
	model = MODEL_BY_DIFICULTY.get(task_dificulty)

	if not model:
		raise ValueError('Model not Found')

	return ChatGroq(
		model=model,
		temperature=0.3,
		api_key=settings.GROQ_API_KEY,
	)