"""
Pruebas unitarias para los endpoints de autenticación.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient

from src.routers.auth import auth_router
from src.schemas.user import User, UserLogin, ChangePassword, ResetPassword

@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba."""
    return TestClient(auth_router)

@pytest.fixture
def mock_auth_repo():
    """Fixture para crear un mock del repositorio de autenticación."""
    with patch('src.routers.auth.AuthRepository') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_auth_handler():
    """Fixture para crear un mock del manejador JWT."""
    with patch('src.routers.auth.auth_handler') as mock:
        yield mock

class TestAuthRouter:
    """Clase para probar los endpoints de autenticación."""
    
    def test_verify_email_success(self, client, mock_auth_repo):
        """Probar la verificación exitosa de un email."""
        # Configurar el mock del repositorio de autenticación
        mock_auth_repo.verify_email.return_value = {"message": "Email verificado exitosamente"}
        
        # Realizar la solicitud
        response = client.post("/verify_email", json={
            "email": "test@example.com",
            "verification_code": "123456"
        })
        
        # Verificar la respuesta
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Email verificado exitosamente"}
    
    def test_register_user_success(self, client, mock_auth_repo):
        """Probar el registro exitoso de un usuario."""
        # Crear datos de prueba
        user_data = {
            "email": "test@example.com",
            "id_number": "123456789",
            "password": "password123",
            "user_name": "testuser",
            "name": "Test User",
            "phone": "12345678",
            "address": "Test Address",
            "birth_date": "2000-01-01",
            "gender": "m"
        }
        
        # Configurar el mock del repositorio de autenticación
        mock_user = MagicMock()
        mock_user.message = "Usuario registrado exitosamente. Por favor verifica tu email."
        mock_auth_repo.register_user.return_value = mock_user
        
        # Realizar la solicitud
        response = client.post("/register", json=user_data)
        
        # Verificar la respuesta
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "Usuario registrado exitosamente. Por favor verifica tu email."
    
    def test_refresh_token_success(self, client, mock_auth_handler):
        """Probar la actualización exitosa del token."""
        # Configurar el mock del manejador JWT
        mock_auth_handler.refresh_token.return_value = "new_access_token"
        
        # Realizar la solicitud
        response = client.get("/refresh_token", headers={"Authorization": "Bearer refresh_token"})
        
        # Verificar la respuesta
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"access_token": "new_access_token"}
    
    def test_get_user_data_success(self, client, mock_auth_handler):
        """Probar la obtención exitosa de datos del usuario."""
        # Configurar el mock del manejador JWT
        mock_auth_handler.decode_token.return_value = {
            "sub": "test@example.com",
            "user.name": "Test User"
        }
        
        # Realizar la solicitud
        response = client.get("/user_data", headers={"Authorization": "Bearer token"})
        
        # Verificar la respuesta
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User found"
        assert response.json()["data"]["sub"] == "test@example.com"
    
    def test_get_user_data_error(self, client, mock_auth_handler):
        """Probar la obtención de datos del usuario con error."""
        # Configurar el mock del manejador JWT para simular un error
        mock_auth_handler.decode_token.side_effect = Exception("Invalid token")
        
        # Realizar la solicitud
        response = client.get("/user_data", headers={"Authorization": "Bearer token"})
        
        # Verificar la respuesta
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Invalid token"
        assert response.json()["data"] is None 