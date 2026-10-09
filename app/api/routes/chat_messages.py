from fastapi import APIRouter, HTTPException

from app.agents.teacher_agent.model import AgentInput
from app.agents.teacher_agent.utils import generate_ai_response

from gpt_teacher_db.gpt_teacher.models.chat_message import ChatMessageCreate
from gpt_teacher_db.gpt_teacher.enum import MessageType, TeachingMethodology

from app.api.deps import SessionDep, CurrentStudentUser
from app.schemas.chat_message import ChatMessagePublicWithTimestamp
from app.cruds import chat_message as message_crud
from app.cruds import student_session as session_crud
from app.cruds import problem as problem_crud
from app.cruds import classroom as classroom_crud


router = APIRouter(tags=['chat-messages'])


@router.post(
	'/call-agent/student-session/{session_id}/chat-messages',
	response_model=ChatMessagePublicWithTimestamp,
)
def send_chat_message(
	session: SessionDep,
	current_user: CurrentStudentUser,
	session_id: str,
	agent_input: AgentInput,
):
	student_session = session_crud.get_student_session_by_id(
		session, session_id
	)
	if not student_session:
		raise HTTPException(status_code=404, detail='Session not found')

	if student_session.student_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to access this session'
		)

	if student_session.status.value != 'open':
		raise HTTPException(status_code=400, detail='Session is not active')

	problem = problem_crud.get_problem_by_id(
		session, student_session.problem_id
	)
	if not problem:
		raise HTTPException(status_code=404, detail='Problem not found')

	# Mensagem do aluno
	user_message_in = ChatMessageCreate(
		session_id=student_session.id,
		problem_id=student_session.problem_id,
		type=MessageType.USER,
		content=agent_input.user_message,
		code=agent_input.student_code,
	)
	message_crud.create_chat_message(session, user_message_in)

	classroom_student = classroom_crud.get_classroom_student(
		session, problem.classroom_id, current_user.id
	)
	methodology = (
		classroom_student.methodology
		if classroom_student
		else TeachingMethodology.SOCRATIC
	)

	teacher_agent_input = AgentInput(
		problem_title=problem.title,
		problem_description=problem.description,
		problem_category=problem.category,
		session_id=agent_input.session_id,
		student_code=agent_input.student_code,
		user_message=agent_input.user_message,
		methodology=methodology,
	)

	# Resposta da IA
	ai_response_content = generate_ai_response(teacher_agent_input)

	ai_message_in = ChatMessageCreate(
		session_id=student_session.id,
		problem_id=student_session.problem_id,
		type=MessageType.AI,
		content=ai_response_content,
	)
	ai_message = message_crud.create_chat_message(session, ai_message_in)

	return ai_message


@router.get(
	'/student-session/{session_id}/chat-messages',
	response_model=list[ChatMessagePublicWithTimestamp],
)
def get_chat_messages(
	session: SessionDep,
	current_user: CurrentStudentUser,
	session_id: str,
):
	"""
	Lista mensagens da sessão
	"""
	student_session = session_crud.get_student_session_by_id(
		session, session_id
	)
	if not student_session:
		raise HTTPException(status_code=404, detail='Session not found')

	if student_session.student_id != current_user.id:
		raise HTTPException(
			status_code=403, detail='Not authorized to access this session'
		)

	messages = message_crud.get_messages_by_session(session, session_id)
	return messages