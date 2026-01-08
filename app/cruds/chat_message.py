from sqlmodel import Session, select

from gpt_teacher_db.gpt_teacher.models.chat_message import (
    ChatMessage,
    ChatMessageCreate,
)


def create_chat_message(
    session: Session, message_in: ChatMessageCreate, session_id: str
) -> ChatMessage:
    """Cria uma nova mensagem no chat"""
    chat_message = ChatMessage(
        session_id=session_id,
        content=message_in.content,
        role=message_in.role,
    )
    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)
    return chat_message


def get_messages_by_session(session: Session, session_id: str) -> list[ChatMessage]:
    """Lista todas as mensagens de uma sessão"""
    statement = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )

    return list(session.exec(statement).all())
