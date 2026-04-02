import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.core.config import settings
from app.api.deps import get_db, get_current_student_user
from app.api.routes import chat_messages as chat_router_module # Importante para o mock
from gpt_teacher_db.gpt_teacher.models.student import Student

client = TestClient(app)

# 1. Setup Global de Mocks (Overrides)
def setup_module():
    app.dependency_overrides[get_db] = lambda: MagicMock()
    app.dependency_overrides[get_current_student_user] = lambda: Student(
        id="12345", name="Test Student", is_active=True
    )

def test_send_chat_message_success(monkeypatch):
    # 2. Mock do CRUD de Sessão
    from app.cruds import student_session, chat_message
    mock_session = MagicMock()
    mock_session.id = uuid.uuid4()
    mock_session.problem_id = uuid.uuid4()
    mock_session.student_id = "12345"
    mock_session.is_active = True
    
    monkeypatch.setattr(student_session, "get_student_session_by_id", lambda s, id: mock_session)
    
    # 3. Mock do CRUD de Mensagem (retorno fake)
    fake_msg_id = uuid.uuid4()
    fake_msg = {
        "id": str(fake_msg_id),
        "session_id": str(mock_session.id),
        "problem_id": str(mock_session.problem_id),
        "content": "Resposta da IA",
        "role": "assistant",
        "type": "ai",          
        "code": "",           
        "code_review": ""      
    }
    monkeypatch.setattr(chat_message, "create_chat_message", lambda s, msg, id: fake_msg)

    # 4. Mock da IA (Apontando para call_teacher_agent dentro do router)
    monkeypatch.setattr(chat_router_module, "call_teacher_agent", lambda x: "Resposta mockada com sucesso")

    # 5. A Chamada com a URL CORRETA (usando o prefixo do settings)
    url = f"{settings.API_V1_STR}/call-agent/student-session/s1/chat-messages"
    payload = {
        "problem_title": "Soma de dois números",
        "problem_description": "Crie uma função que some A e B",
        "is_sandbox": False,
        "student_code": "def soma(a, b): return a + b",
        "user_message": "Olá, professor! Meu código está certo?",
        "session_id": str(mock_session.id)
    }
    
    response = client.post(url, json=payload)

    # 6. Validações
    assert response.status_code == 200
    assert response.json()["content"] == "Resposta da IA"