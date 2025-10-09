from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UserCreate, UserLogin, UserResponse, Token
from app.db.database import get_db_session
from app.repository.user_repo import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_repo(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthService(user_repo)

@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register(
    user_data: UserCreate, 
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Creates a new user account.
    - Validates input via Pydantic schema (UserCreate).
    - Uses AuthService to hash the password and save to DB.
    """
    try:
        new_user = await auth_service.register_user(user_data)
        return new_user
    except HTTPException as e:
        raise e

@router.post(
    "/login", 
    response_model=Token, 
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and get JWT token"
)
async def login(
    credentials: UserLogin, 
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticates user credentials.
    - Uses AuthService to verify password and generate a JWT.
    """
    token = await auth_service.authenticate_user(credentials)
    return token