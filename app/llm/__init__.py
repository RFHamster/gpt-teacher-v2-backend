from langchain_groq import ChatGroq


class GroqModels(str):
	LOW = 'llama-3.3-8b'
	MEDIUM = 'llama-3.3-70b-versatile'
	HIGH = 'mixtral-8x7b-32768'


MODEL_BY_DIFICULTY = {
	'LOW': GroqModels.LOW,
	'MEDIUM': GroqModels.MEDIUM,
	'HIGH': GroqModels.HIGH,
}


def get_model_by_difficulty(task_dificulty: str) -> ChatGroq:
	model = MODEL_BY_DIFICULTY.get(task_dificulty)

	if not model:
		raise ValueError('Model not Found')

	return ChatGroq(model=model, temperature=0.3)
