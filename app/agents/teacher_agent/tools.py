from langchain_core.tools import tool
from langgraph.store.base import BaseStore
from typing import Annotated
from langgraph.prebuilt import InjectedState, ToolRuntime
from langchain_core.runnables import RunnableConfig
from dataclasses import dataclass

@dataclass
class Context:
    student_id: str
    concept: str
    mastery_level: str

@tool
def save_student_knowledge(
    user_info: Context, 
    store: Annotated[BaseStore, InjectedState("store")],
    config: RunnableConfig
) -> str:
    """
    Registra que o aluno aprendeu ou tem dificuldade em um conceito específico.
    Ex: concept='ponteiros', mastery_level='baixo'
    """
    
    student_id = config["configurable"].get("student_id")
    
    store.put(("users",), student_id, dict(user_info))
    
    return "Informação salva."

    


@tool
def get_student_history(
    runtime: ToolRuntime[Context]
) -> str:
    """Busca o histórico, preferências e dificuldades salvas do aluno."""
    namespace = ("students", runtime.context.student_id)
    memories = runtime.store.search(namespace)
    
    if not memories:
        return "Ainda não tenho registros históricos sobre este aluno."
    
    history = "\n".join([f"- {m.key}: {m.value}" for m in memories])
    return f"Aqui está o que eu lembro sobre o aluno:\n{history}"