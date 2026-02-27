from fastapi import APIRouter, HTTPException
from app.agents.model import (
    generate_ai_response,
    AgentInput
)

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
    "/call-agent/student-session/{session_id}",
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
    
    if agent_input.create_student_message:
        user_message = message_crud.create_chat_message(session, agent_input.student_input, session_id)
    else:
        user_message = ChatMessage(
            content=agent_input.student_input,
            role="user",
            student_session_id=session_id,
        )

    ai_response_content = generate_ai_response(student_session, user_message, problem, agent_input.student_code)

    ai_message_in = ChatMessageCreate(
        content=ai_response_content,
        role="assistant",
    )
    ai_message = message_crud.create_chat_message(session, ai_message_in, session_id)

    return ai_message
    

@router.post(
    "/student-sessions/{session_id}/chat-messages",
    response_model=list[ChatMessagePublic],
)
def send_chat_message(
    session: SessionDep,
    current_user: CurrentStudentUser,
    session_id: str,
    message_in: ChatMessageCreate,
):
    """
    Envia mensagem (aluno envia, IA responde)
    """
    # Verifica se a sessão existe e pertence ao aluno
    student_session = session_crud.get_student_session_by_id(session, session_id)
    if not student_session:
        raise HTTPException(status_code=404, detail="Session not found")

    if student_session.student_id != str(current_user.id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this session"
        )

    if not student_session.is_active:
        raise HTTPException(status_code=400, detail="Session is not active")

    # Cria mensagem do usuário
    user_message = message_crud.create_chat_message(session, message_in, session_id)

    # Gerar resposta da IA
    ai_response_content = generate_ai_response(student_session, user_message)

    ai_message_in = ChatMessageCreate(
        content=ai_response_content,
        role="assistant",
    )
    ai_message = message_crud.create_chat_message(session, ai_message_in, session_id)

    # Retorna ambas as mensagens (usuário + IA)
    return [user_message, ai_message]


@router.get(
    "/student-sessions/{session_id}/chat-messages",
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
