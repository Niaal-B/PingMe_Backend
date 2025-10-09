from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.db.models import User
from app.repository.user_repo import UserRepository
from app.core.security import decode_token, ACCESS_TOKEN_TYPE


bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), 
    session: AsyncSession = Depends(get_db_session)
) -> User:
    """
    General dependency to validate the Access Token and retrieve the User object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception
    
    token = credentials.credentials 
    payload = decode_token(token)
    
    if payload is None or payload.get("type") != ACCESS_TOKEN_TYPE:
        raise credentials_exception

    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    user_repo = UserRepository(session)
    user = await user_repo.get_user_by_id(user_id)
    
    if user is None or not user.is_active:
        raise credentials_exception
        
    return user