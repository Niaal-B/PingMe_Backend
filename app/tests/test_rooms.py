import pytest
from fastapi import status


class TestRoomCreation:
    
    def test_create_room_success(self, client, auth_token):
        room_data = {"room_name": "Test Room"}
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = client.post("/rooms/", json=room_data, headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["room_name"] == "Test Room"
        assert "id" in data
        assert "created_by" in data
    
    def test_create_room_without_auth_fails(self, client):
        room_data = {"room_name": "Unauthorized Room"}
        response = client.post("/rooms/", json=room_data)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    def test_create_duplicate_room_name_fails(self, client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        room_data = {"room_name": "Duplicate Room"}
        
        client.post("/rooms/", json=room_data, headers=headers)
        response = client.post("/rooms/", json=room_data, headers=headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"].lower()


class TestGetRooms:
    
    def test_get_all_rooms(self, client, auth_token, db_session):
        from app.models.user import User
        from app.models.room import Room
        
        user2 = User(
            username="user2",
            email="user2@example.com",
            hashed_password="$2b$12$ENw8bWAXl7I5UVPZX9yy7.uWwwDRtUI6c0NqlxPuUf9lHcye1Njg."
        )
        db_session.add(user2)
        db_session.commit()
        
        room = Room(room_name="Other User Room", created_by=user2.id)
        db_session.add(room)
        db_session.commit()
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/rooms/", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        rooms = response.json()
        assert isinstance(rooms, list)
        assert len(rooms) > 0
    
    def test_get_my_rooms(self, client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        client.post("/rooms/", json={"room_name": "My Room"}, headers=headers)
        
        response = client.get("/rooms/my", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        rooms = response.json()
        assert isinstance(rooms, list)
        assert len(rooms) > 0


class TestDeleteRoom:
    
    def test_delete_room_success(self, client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        create_response = client.post("/rooms/", json={"room_name": "To Delete"}, headers=headers)
        room_id = create_response.json()["id"]
        
        delete_response = client.delete(f"/rooms/{room_id}", headers=headers)
        
        assert delete_response.status_code == status.HTTP_200_OK
        assert "deleted successfully" in delete_response.json()["detail"].lower()
    
    def test_delete_nonexistent_room_fails(self, client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.delete("/rooms/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_other_user_room_fails(self, client, auth_token, db_session):
        from app.models.user import User
        from app.models.room import Room
        
        user2 = User(
            username="user2",
            email="user2@example.com",
            hashed_password="$2b$12$ENw8bWAXl7I5UVPZX9yy7.uWwwDRtUI6c0NqlxPuUf9lHcye1Njg."
        )
        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user2)
        
        room = Room(room_name="User2 Room", created_by=user2.id)
        db_session.add(room)
        db_session.commit()
        db_session.refresh(room)
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.delete(f"/rooms/{room.id}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

