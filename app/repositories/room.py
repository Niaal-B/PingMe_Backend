from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import RoomCreate
from fastapi import HTTPException
from typing import List

def create_room(db: Session, room_data: RoomCreate, user_id: int) -> Room:
    existing = db.query(Room).filter(Room.room_name == room_data.room_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room name already exists")

    new_room = Room(
        room_name=room_data.room_name,
        created_by=user_id
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


def get_all_rooms(db: Session) -> List[Room]:
    return db.query(Room).order_by(Room.created_at.desc()).all()