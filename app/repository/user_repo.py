from sqlalchemy import select,or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.api.schemas import UserCreate 

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: dict) -> User:
        """Saves a new User object to the database."""
        db_user = User(**user_data)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user) 
        return db_user

    async def get_user_by_email_or_name(self, email: str, name: str) -> User | None:
        """Retrieves a user by their unique email address or username."""
        stmt = select(User).where(or_(User.email==email,User.username==name))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieves a user by their primary key ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()