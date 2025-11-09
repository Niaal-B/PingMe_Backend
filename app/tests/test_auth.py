import pytest
from fastapi import status


class TestUserRegistration:
    
    def test_register_new_user_success(self, client):
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert data["id"] is not None
    
    def test_register_duplicate_email_fails(self, client):
        first_user = {
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "password123"
        }
        client.post("/auth/register", json=first_user)
        
        duplicate_user = {
            "username": "user2",
            "email": "duplicate@example.com",
            "password": "password456"
        }
        response = client.post("/auth/register", json=duplicate_user)
        
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
        detail = response.json().get("detail", "")
        detail_str = str(detail).lower()
        assert "already" in detail_str or "exists" in detail_str or "registered" in detail_str
    
    def test_register_duplicate_username_fails(self, client):
        first_user = {
            "username": "sameusername",
            "email": "user1@example.com",
            "password": "password123"
        }
        client.post("/auth/register", json=first_user)
        
        duplicate_user = {
            "username": "sameusername",
            "email": "user2@example.com",
            "password": "password456"
        }
        response = client.post("/auth/register", json=duplicate_user)
        
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
        detail = response.json().get("detail", "")
        detail_str = str(detail).lower()
        assert "already" in detail_str or "exists" in detail_str or "registered" in detail_str


class TestUserLogin:
    
    def test_login_with_correct_credentials(self, client, test_user):
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert len(data["access_token"]) > 0
    
    def test_login_with_wrong_password_fails(self, client, test_user):
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid" in response.json()["detail"].lower()
    
    def test_login_with_nonexistent_email_fails(self, client):
        login_data = {
            "email": "nonexistent@example.com",
            "password": "anypassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid" in response.json()["detail"].lower()


class TestProtectedEndpoints:
    
    def test_get_me_with_valid_token(self, client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data
    
    def test_get_me_without_token_fails(self, client):
        response = client.get("/auth/me")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    def test_get_me_with_invalid_token_fails(self, client):
        headers = {"Authorization": "Bearer fake_token_12345"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

