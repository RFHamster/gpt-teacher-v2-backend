from app.llm import get_model_by_difficulty
from app.agents.teacher_agent.prompt import SYSTEM_PROMPT
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.language_models import BaseChatModel
from langchain.agents import create_agent
from app.agents.teacher_agent.model import AgentInput


TASK_DIFFICULTY = 'MEDIUM'


def get_prompt(
	*,
	problem_title: str,
	problem_description: str,
	is_sandbox: bool,
	student_code: str,
) -> str:
	return SYSTEM_PROMPT.format(
		{
			'problem_title': problem_title,
			'problem_description': problem_description,
			'is_sandbox': str(is_sandbox),
			'student_code': student_code,
		}
	)


def get_tools() -> list:
	return []


def get_teacher_agent(
	*,
	problem_title: str,
	problem_description: str,
	is_sandbox: bool,
	student_code: str,
) -> BaseChatModel:
	model = get_model_by_difficulty(TASK_DIFFICULTY)

	return create_agent(
		model=model,
		tools=get_tools(),
		system_prompt=get_prompt(
			problem_title=problem_title,
			problem_description=problem_description,
			is_sandbox=is_sandbox,
			student_code=student_code,
		),
	)


def call_teacher_agent(agent_input: AgentInput) -> str:
	brain = get_teacher_agent(
		problem_title=agent_input.problem_title,
		problem_description=agent_input.problem_description,
		is_sandbox=agent_input.is_sandbox,
		student_code=agent_input.student_code,
	)
	response = brain.invoke(HumanMessage())

	return response.content
