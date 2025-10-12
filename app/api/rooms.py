from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import RoomCreate, RoomResponse
from app.db.database import get_db_session
from app.db.models import User
from app.repository.room_repo import RoomRepository
from app.services.room_service import RoomService
from app.core.dependencies import get_current_user 

router = APIRouter(prefix="/rooms", tags=["Rooms"])

def get_room_repo(session: AsyncSession = Depends(get_db_session)) -> RoomRepository:
    return RoomRepository(session)

def get_room_service(room_repo: RoomRepository = Depends(get_room_repo)) -> RoomService:
    return RoomService(room_repo)

@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new chat room"
)
async def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    room_service: RoomService = Depends(get_room_service)
):
    new_room = await room_service.create_new_room(room_data.name, current_user)
    return new_room

@router.get(
    "/",
    response_model=list[RoomResponse],
    summary="List all available chat rooms"
)
async def list_rooms(
    current_user: User = Depends(get_current_user),
    room_service: RoomService = Depends(get_room_service)
):
    rooms = await room_service.get_available_rooms()
    return rooms