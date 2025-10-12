from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Room

class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_room(self, name: str) -> Room:
        db_room = Room(name=name)
        self.session.add(db_room)
        await self.session.commit()
        await self.session.refresh(db_room)
        return db_room

    async def get_room_by_name(self, name: str) -> Room | None:
        stmt = select(Room).where(Room.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_rooms(self) -> list[Room]:
        stmt = select(Room).order_by(Room.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()