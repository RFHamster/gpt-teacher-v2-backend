from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import (
    auth,
    teachers,
    students,
    classrooms,
    problems,
    student_sessions,
    chat_messages,
    consolidations,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth")
app.include_router(teachers.router, prefix=f"{settings.API_V1_STR}/teachers")
app.include_router(students.router, prefix=f"{settings.API_V1_STR}/students")
app.include_router(classrooms.router, prefix=f"{settings.API_V1_STR}/classrooms")
app.include_router(problems.router, prefix=f"{settings.API_V1_STR}")
app.include_router(
    student_sessions.router, prefix=f"{settings.API_V1_STR}/student-sessions"
)
app.include_router(chat_messages.router, prefix=f"{settings.API_V1_STR}")
app.include_router(consolidations.router, prefix=f"{settings.API_V1_STR}")


@app.get("/")
def root():
    return {"message": "GPT Teacher Backend API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
