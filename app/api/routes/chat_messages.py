from fastapi import APIRouter, HTTPException
from app.agents.teacher_agent.model import AgentInput
from app.agents.teacher_agent import call_teacher_agent


from gpt_teacher_db.gpt_teacher.models.chat_message import (
    ChatMessage,
    ChatMessageCreate,
    ChatMessagePublic
)

from app.api.deps import SessionDep, CurrentStudentUser
from app.cruds import chat_message as message_crud
from app.cruds import student_session as session_crud


router = APIRouter(tags=["chat-messages"])


@router.post(
    "/call-agent/student-session/{session_id}/chat-messages",
    response_model=ChatMessagePublic,
)
def send_chat_message(
    session: SessionDep,
    current_user: CurrentStudentUser,
    session_id: str,
    agent_input: AgentInput,
):
    
    student_session = session_crud.get_student_session_by_id(session, session_id)
    if not student_session:
        raise HTTPException(status_code=404, detail="Session not found")

    if student_session.student_id != str(current_user.id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this session"
        )

    if not student_session.is_active:
        raise HTTPException(status_code=400, detail="Session is not active")
    
    message_crud.create_chat_message(session, agent_input.user_message, session_id)    

    ai_response_content = call_teacher_agent(agent_input)

    ai_message_in = ChatMessageCreate(
        content=ai_response_content,
        role="assistant",
        session_id=student_session.id,      
        problem_id=student_session.problem_id 
    )
    ai_message = message_crud.create_chat_message(session, ai_message_in, session_id)

    return ai_message

@router.get(
    "/student-session/{session_id}/chat-messages",
    response_model=list[ChatMessagePublic],
)
def get_chat_messages(
    session: SessionDep,
    current_user: CurrentStudentUser,
    session_id: str,
):
    """
    Lista mensagens da sessão
    """
    # Verifica se a sessão existe e pertence ao aluno
    student_session = session_crud.get_student_session_by_id(session, session_id)
    if not student_session:
        raise HTTPException(status_code=404, detail="Session not found")

    if student_session.student_id != str(current_user.id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this session"
        )

    messages = message_crud.get_messages_by_session(session, session_id)
    return messages
