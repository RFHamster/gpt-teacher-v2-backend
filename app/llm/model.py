from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.api.routes import get_chat_messages
from .prompt import SYSTEM_PROMPT
from gpt_teacher_db.gpt_teacher.models.problem import Problem

def get_llm():
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_message}") 
    ])

    chain = prompt | llm

    return RunnableWithMessageHistory(
        chain,
        get_chat_messages,
        input_messages_key="user_message", 
        history_messages_key="chat_history",
    )

def generate_ai_response(student_session: str, user_message: str, problem: Problem, student_code: str) -> str:
    brain = get_llm()

    full_input = {
        "problem_title": problem.title,
        "problem_description": problem.description or "Sem descrição.",
        "is_sandbox": "Sim" if problem.is_sandbox else "Não",
        "student_code": student_code,
        "user_message": user_message 
    }

    response = brain.invoke(
        full_input,
        config={"configurable": {"session_id": student_session}}
    )
    
    return response.content