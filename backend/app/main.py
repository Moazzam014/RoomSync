from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine

# Import all models before creating tables
from app.models import (
    User,
    Room,
    Member,
    Task,
    Presence,
    Rotation,
    Notification,
    TaskExemption,
)

# Import API routers
from app.api.rooms import router as rooms_router
from app.api.members import router as members_router
from app.api.tasks import router as tasks_router
from app.api.workflow import router as workflow_router
from app.api.presence import router as presence_router
from app.api.notifications import router as notifications_router
from app.api.auth import router as auth_router
from app.api.invitations import router as invitations_router
from app.api.my_rooms import router as my_rooms_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables automatically only in development.
    # Tests and production must use controlled database setup/migrations.
    if settings.APP_ENV == "development":
        Base.metadata.create_all(bind=engine)

    yield

    # Application shutdown cleanup can be added here if required.


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)


# CORS configuration
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


# Register API routers
app.include_router(rooms_router)
app.include_router(members_router)
app.include_router(tasks_router)
app.include_router(workflow_router)
app.include_router(presence_router)
app.include_router(notifications_router)
app.include_router(auth_router)
app.include_router(invitations_router)
app.include_router(my_rooms_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "RoomSync backend is running successfully!"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }

    finally:
        db.close()