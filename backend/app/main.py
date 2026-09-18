from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import Base, SessionLocal

# Import all models before creating tables
from app.models import (
    Room,
    Member,
    Task,
    Presence,
    Rotation,
    Notification,
    TaskExemption,
)

from app.api.rooms import router as rooms_router
from app.api.members import router as members_router
from app.api.tasks import router as tasks_router
from app.api.workflow import router as workflow_router
from app.api.presence import router as presence_router
from app.api.notifications import router as notifications_router
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=SessionLocal.kw["bind"])


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(rooms_router)
app.include_router(members_router)
app.include_router(tasks_router)
app.include_router(workflow_router)
app.include_router(presence_router)
app.include_router(notifications_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "RoomSync backend is running successfully!"
    }


@app.get("/health")
def health_check():
    try:
        db = SessionLocal()

        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }

    finally:
        if "db" in locals():
            db.close()