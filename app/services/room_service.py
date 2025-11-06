from sqlalchemy.orm import Session
from app.schemas.room import RoomCreate
from app.repositories.room import create_room,get_all_rooms,get_my_rooms

def create_room_service(db: Session, room_data: RoomCreate, user_id: int):
    return create_room(db, room_data, user_id)

def get_all_rooms_service(db: Session, user_id: int):
    return get_all_rooms(db, user_id)

def get_my_rooms_service(db: Session, user_id: int):
    return get_my_rooms(db, user_id)