from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user import get_user_by_email, create_user
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse

def register_user(user: UserCreate, db: Session):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    return create_user(db, user, hashed_pw)

def login_user(email: str, password: str, db: Session) -> TokenResponse:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token)
