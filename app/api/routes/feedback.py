from uuid import UUID

import httpx
from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentTeacherUser
from app.core.config import settings

router = APIRouter(tags=['feedback'])

_HEADERS = {'X-Internal-API-Key': settings.INTERNAL_API_KEY}


def _proxy_get(path: str, teacher_id: UUID) -> dict:
	url = f'{settings.FEEDBACK_SERVICE_URL}{settings.API_V1_STR}{path}'
	try:
		resp = httpx.get(
			url,
			headers=_HEADERS,
			params={'teacher_id': str(teacher_id)},
			timeout=10.0,
		)
	except httpx.RequestError as exc:
		raise HTTPException(
			status_code=503,
			detail=f'Feedback service unavailable: {exc}',
		)
	if resp.status_code >= 400:
		raise HTTPException(status_code=resp.status_code, detail=resp.text)
	return resp.json()


@router.post('/feedback/generate', status_code=202)
def trigger_feedback_generation(current_user: CurrentTeacherUser):
	url = f'{settings.FEEDBACK_SERVICE_URL}{settings.API_V1_STR}/feedback/generate'
	try:
		resp = httpx.post(url, headers=_HEADERS, timeout=10.0)
	except httpx.RequestError as exc:
		raise HTTPException(status_code=503, detail=f'Feedback service unavailable: {exc}')
	if resp.status_code >= 400:
		raise HTTPException(status_code=resp.status_code, detail=resp.text)
	return resp.json()


@router.get('/classrooms/{classroom_id}/feedback/summary')
def get_classroom_feedback_summary(
	classroom_id: UUID,
	current_user: CurrentTeacherUser,
):
	return _proxy_get(
		f'/feedback/classrooms/{classroom_id}/summary',
		current_user.id,
	)


@router.get('/classrooms/{classroom_id}/students/{student_id}/feedback')
def get_student_feedback(
	classroom_id: UUID,
	student_id: UUID,
	current_user: CurrentTeacherUser,
):
	return _proxy_get(
		f'/feedback/classrooms/{classroom_id}/students/{student_id}',
		current_user.id,
	)


@router.get('/sessions/{session_id}/feedback')
def get_session_feedback(
	session_id: UUID,
	current_user: CurrentTeacherUser,
):
	return _proxy_get(
		f'/feedback/sessions/{session_id}',
		current_user.id,
	)
