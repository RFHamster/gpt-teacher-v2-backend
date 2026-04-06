from langchain.messages import HumanMessage

from app.llm import get_model_by_difficulty
from app.agents.teacher_agent.prompt import SYSTEM_PROMPT
from langchain_core.language_models import BaseChatModel
from langchain.agents import create_agent
from app.agents.teacher_agent.model import AgentInput
from app.llm.db import get_db_uri
from langgraph.checkpoint.postgres import PostgresSaver

TASK_DIFFICULTY = 'MEDIUM'


def get_prompt(
	*,
	problem_title: str,
	problem_description: str
) -> str:
	return SYSTEM_PROMPT.format(
		**{
			'problem_title': problem_title,
			'problem_description': problem_description
		}
	)


def get_tools() -> list:
	return []


def get_teacher_agent(
	*,
	problem_title: str,
	problem_description: str, 
	checkpointer: PostgresSaver = None
) -> BaseChatModel:
	model = get_model_by_difficulty(TASK_DIFFICULTY)
		
	return create_agent(
		model=model,
		tools=get_tools(),
		checkpointer=checkpointer,
		system_prompt=get_prompt(
			problem_title=problem_title,
			problem_description=problem_description
		)
	)


def call_teacher_agent(agent_input: AgentInput) -> str:
	DB_URI = get_db_uri()

	with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
		checkpointer.setup()
	
		brain = get_teacher_agent(
			problem_title=agent_input.problem_title,
			problem_description=agent_input.problem_description, 
			checkpointer=checkpointer
		)
	
		response = brain.invoke(
			{
				'messages': [
					HumanMessage(
						content=f'* Código do Aluno: <student_code>{agent_input.student_code}</student_code>\n* Mensagem do Aluno: <student_message>{agent_input.user_message}</student_message>'
					)
				]
			},
			{'configurable': {'thread_id': agent_input.session_id}},
		)

		return response['messages'][-1].content
