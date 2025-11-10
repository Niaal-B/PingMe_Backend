from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.room import RoomCreate, RoomOut
from app.dependencies.auth import get_current_user
from app.services.room_service import create_room_service,get_all_rooms_service,get_my_rooms_service,delete_room_service
from app.database import get_db
from typing import List

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("", response_model=RoomOut)
def create_new_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_room_service(db, room_data, current_user.id)


@router.get("", response_model=List[RoomOut])
def get_all_rooms(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all_rooms_service(db,current_user.id)


@router.get("/my")
def get_my_rooms_endpoint(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_my_rooms_service(db, current_user.id)


@router.delete("/{room_id}")
def delete_room_endpoint(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = delete_room_service(db, room_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Room not found or unauthorized")
    return {"detail": "Room deleted successfully"}
