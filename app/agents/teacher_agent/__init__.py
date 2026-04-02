from langchain.messages import HumanMessage

from app.llm import get_model_by_difficulty
from app.agents.teacher_agent.prompt import SYSTEM_PROMPT
from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph
from langchain.agents import create_agent
from app.agents.teacher_agent.model import AgentInput
from app.llm.memory import get_db_resources
from app.agents.teacher_agent.tools import (
    save_student_knowledge, 
    get_student_history
)

TASK_DIFFICULTY = 'MEDIUM'

def get_prompt(*, problem_title: str, problem_description: str) -> str:
    return SYSTEM_PROMPT.format(**{
        "problem_title": problem_title,
        "problem_description": problem_description,
    })


def get_tools() -> list:
    return [save_student_knowledge, get_student_history]


def get_teacher_agent(
    *, 
    problem_title: str, 
    problem_description: str
) -> CompiledStateGraph:
    
    model = get_model_by_difficulty(TASK_DIFFICULTY)
    
    system_prompt = get_prompt(
        problem_title=problem_title, 
        problem_description=problem_description
    )

    checkpointer, store = get_db_resources()

    agent = create_agent(
        model=model,
        tools=get_tools(),
        checkpointer=checkpointer,
        store=store,
        system_prompt=system_prompt
    )
    
    return agent


def call_teacher_agent(agent_input: AgentInput) -> str:
    brain = get_teacher_agent(
        problem_title=agent_input.problem_title,
        problem_description=agent_input.problem_description
    )

    config = {
        "configurable": {
            "thread_id": agent_input.session_id,
            "student_id": agent_input.student_id
            }
        }
    
    input_data = {
        "messages": [
				HumanMessage(
					content=f'* Código do Aluno: <student_code>{agent_input.student_code}</student_code>\n* Mensagem do Aluno: <student_message>{agent_input.user_message}</student_message>'
				)
			]
        }
    response = brain.invoke(input_data, config=config)
    
    return response["messages"][-1].content
