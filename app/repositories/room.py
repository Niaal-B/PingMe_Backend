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


def get_all_rooms(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Room]:
    return (
        db.query(Room)
        .filter(Room.created_by != user_id)
        .order_by(Room.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_my_rooms(db: Session, user_id: int) -> List[Room]:
    return (
        db.query(Room)
        .filter(Room.created_by == user_id)
        .order_by(Room.created_at.desc())
        .all()
    )


def delete_room(db: Session, room_id: int, user_id: int):
    room = db.query(Room).filter(Room.id == room_id, Room.created_by == user_id).first()
    if not room:
        return None
    db.delete(room)
    db.commit()
    return room
