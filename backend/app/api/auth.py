from fastapi import APIRouter

from app.schemas.auth import LoginRequest, TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(login_data: LoginRequest):
    return {
        "access_token": "roomsync-development-token",
        "token_type": "bearer",
    }