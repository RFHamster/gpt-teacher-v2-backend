from fastapi import APIRouter, HTTPException

from gpt_teacher_db.gpt_teacher.models.chat_message import (
    ChatMessage,
    ChatMessageCreate,
    ChatMessagePublic,
)

from app.api.deps import SessionDep, CurrentStudentUser
from app.cruds import chat_message as message_crud
from app.cruds import student_session as session_crud


router = APIRouter(tags=["chat-messages"])


@router.post(
    "/student-session/{session_id}/chat-messages",
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

    # TODO: Gerar resposta da IA
    # ai_response_content = generate_ai_response(student_session, user_message)

    # Por enquanto, vamos criar uma resposta simulada
    ai_response_content = f"Esta é uma resposta da IA para: {message_in.content}"

    ai_message_in = ChatMessageCreate(
        content=ai_response_content,
        role="assistant",
    )
    ai_message = message_crud.create_chat_message(session, ai_message_in, session_id)

    # Retorna ambas as mensagens (usuário + IA)
    return [user_message, ai_message]


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
