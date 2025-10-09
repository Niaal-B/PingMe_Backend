from fastapi import HTTPException, status
from typing import Type
from datetime import timedelta

from app.db.models import User
from app.api.schemas import UserCreate, UserLogin, Token
from app.repository.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_in: UserCreate) -> User:
        
        existing_user = await self.user_repo.get_user_by_email_or_name(user_in.email,user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                
                detail="Email or Username already registered."
            )
        
        hashed_password = hash_password(user_in.password)
        
        user_data = user_in.model_dump(exclude={"password"})
        user_data["hashed_password"] = hashed_password
        
        db_user = await self.user_repo.create_user(user_data)
        return db_user

    async def authenticate_user(self, user_in: UserLogin) -> Token:
        """Authenticates user and returns an access token upon success."""
        
        user = await self.user_repo.get_user_by_email(user_in.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials."
            )

        if not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials."
            )

        access_token_data = {"user_id": user.id}
        access_token = create_access_token(access_token_data)

        return Token(access_token=access_token)
