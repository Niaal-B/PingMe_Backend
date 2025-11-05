from pydantic import BaseModel
from datetime import datetime

class RoomCreate(BaseModel):
    room_name: str

class RoomOut(BaseModel):
    id: int
    room_name: str
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True
