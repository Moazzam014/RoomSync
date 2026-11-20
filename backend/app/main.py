
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine

# Import all models before creating tables.
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

# Import API routers.
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
    # Automatic table creation is development-only.
    # Production and test databases use controlled migrations/setup.
    if settings.APP_ENV == "development":
        Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers.
app.include_router(rooms_router)
app.include_router(members_router)
app.include_router(tasks_router)
app.include_router(workflow_router)
app.include_router(presence_router)
app.include_router(notifications_router)
app.include_router(auth_router)
app.include_router(invitations_router)
app.include_router(my_rooms_router)


@app.get("/")
def root():
    return {
        "message": "RoomSync backend is running successfully!"
    }


@app.get("/health")
def health_check():
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
            },
        )
