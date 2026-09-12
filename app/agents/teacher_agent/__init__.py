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


def get_prompt(
	*,
	problem_title: str,
	problem_description: str,
	problem_category: str | None,
	methodology: TeachingMethodology,
) -> str:
	category_line = f'\nMatéria/Tópico: {problem_category}' if problem_category else ''
	methodology_block = get_methodology_block(methodology)
	return BASE_PROMPT.format(
		**{
			'problem_title': problem_title,
			'problem_description': problem_description,
			'category_line': category_line,
			'methodology_block': methodology_block,
		}
	)


def get_tools() -> list:
	return []


def get_teacher_agent(
	*,
	problem_title: str,
	problem_description: str,
	problem_category: str | None,
	methodology: TeachingMethodology,
	checkpointer: PostgresSaver = None
) -> BaseChatModel:
	model = get_model_by_difficulty(TASK_DIFFICULTY)
	return create_agent(
		model=model,
		tools=get_tools(),
		checkpointer=checkpointer,
		system_prompt=get_prompt(
			problem_title=problem_title,
			problem_description=problem_description,
			problem_category=problem_category,
			methodology=methodology,
		)
	)


def call_teacher_agent(agent_input: AgentInput) -> str:
	DB_URI = get_db_uri()
	with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
		checkpointer.setup()
		brain = get_teacher_agent(
			problem_title=agent_input.problem_title,
			problem_description=agent_input.problem_description,
			problem_category=agent_input.problem_category,
			methodology=agent_input.methodology,
			checkpointer=checkpointer
		)
		response = brain.invoke(
			{
				'messages': [
					HumanMessage(
						content=f'Metodologia do aluno: {agent_input.methodology.value}. Código atual do aluno: {agent_input.student_code}'
					),
					HumanMessage(
						content=agent_input.user_message
					),
				]
			},
			{'configurable': {'thread_id': agent_input.session_id}},
		)
		return response['messages'][-1].content