from langchain.messages import HumanMessage
from app.llm import get_model_by_difficulty
from app.agents.teacher_agent.prompt import BASE_PROMPT, get_methodology_block
from langchain_core.language_models import BaseChatModel
from langchain.agents import create_agent
from app.agents.teacher_agent.model import AgentInput
from app.llm.db import get_db_uri
from langgraph.checkpoint.postgres import PostgresSaver
from gpt_teacher_db.gpt_teacher.enum import TeachingMethodology

TASK_DIFFICULTY = 'MEDIUM'


def get_prompt(*, methodology: TeachingMethodology) -> str:
	methodology_block = get_methodology_block(methodology)
	return BASE_PROMPT.format(methodology_block=methodology_block)


def get_tools() -> list:
	return []


def get_teacher_agent(
	*,
	methodology: TeachingMethodology,
	checkpointer: PostgresSaver = None
) -> BaseChatModel:
	model = get_model_by_difficulty(TASK_DIFFICULTY)
	return create_agent(
		model=model,
		tools=get_tools(),
		checkpointer=checkpointer,
		system_prompt=get_prompt(methodology=methodology)
	)


def call_teacher_agent(agent_input: AgentInput) -> str:
	DB_URI = get_db_uri()
	with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
		checkpointer.setup()
		brain = get_teacher_agent(
			methodology=agent_input.methodology,
			checkpointer=checkpointer
		)
		category = agent_input.problem_category or 'não informada'
		response = brain.invoke(
			{
				'messages': [
					HumanMessage(
						content=(
							f'Metodologia do aluno: {agent_input.methodology.value}. '
							f'Problema: {agent_input.problem_title}. '
							f'Descrição: {agent_input.problem_description}. '
							f'Categoria: {category}. '
							f'Código atual do aluno: {agent_input.student_code}'
						)
					),
					HumanMessage(
						content=agent_input.user_message
					),
				]
			},
			{'configurable': {'thread_id': agent_input.session_id}},
		)
		return response['messages'][-1].content