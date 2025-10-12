from fastapi import HTTPException, status
from app.db.models import Room, User
from app.repository.room_repo import RoomRepository

class RoomService:
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo

    async def create_new_room(self, name: str, user: User) -> Room:
        existing_room = await self.room_repo.get_room_by_name(name)
        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A room with this name already exists."
            )
        
        new_room = await self.room_repo.create_room(name=name)
        return new_room

    async def get_available_rooms(self) -> list[Room]:
        rooms = await self.room_repo.get_all_rooms()
        return rooms
