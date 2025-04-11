"""
Pruebas unitarias para el manejador JWT.
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status

from src.auth.jwt_handler import JWTHandler

# Clave secreta y algoritmo para pruebas
TEST_SECRET = "test_secret"
TEST_ALGORITHM = "HS256"

@pytest.fixture
def jwt_handler():
    """Fixture para crear una instancia del manejador JWT."""
    return JWTHandler(TEST_SECRET, TEST_ALGORITHM)

@pytest.fixture
def mock_user():
    """Fixture para crear un mock de usuario."""
    user = MagicMock()
    user.email = "test@example.com"
    user.name = "Test User"
    user.id_number = "123456789"
    user.role_id = 1
    user.status = True
    user.is_verified = True
    return user

class TestJWTHandler:
    """Clase para probar el manejador JWT."""
    
    def test_hash_password(self, jwt_handler):
        """Probar el hash de contraseña."""
        password = "test_password"
        hashed_password = jwt_handler.hash_password(password)
        
        # Verificar que el hash es diferente a la contraseña original
        assert hashed_password != password
        # Verificar que el hash comienza con el prefijo correcto
        assert hashed_password.startswith("$2b$")
    
    def test_verify_password(self, jwt_handler):
        """Probar la verificación de contraseña."""
        password = "test_password"
        hashed_password = jwt_handler.hash_password(password)
        
        # Verificar que la contraseña es correcta
        assert jwt_handler.verify_password(password, hashed_password) is True
        # Verificar que una contraseña incorrecta no pasa la verificación
        assert jwt_handler.verify_password("wrong_password", hashed_password) is False
    
    def test_encode_token(self, jwt_handler, mock_user):
        """Probar la codificación de token."""
        token = jwt_handler.encode_token(mock_user)
        
        # Verificar que el token es una cadena
        assert isinstance(token, str)
        # Verificar que el token puede ser decodificado
        payload = jwt.decode(token, TEST_SECRET, algorithms=[TEST_ALGORITHM])
        assert payload["sub"] == mock_user.email
        assert payload["user.name"] == mock_user.name
        assert payload["user.id_number"] == mock_user.id_number
        assert payload["user.role"] == mock_user.role_id
        assert payload["user.status"] == mock_user.status
        assert payload["user.is_verified"] == mock_user.is_verified
        assert payload["scope"] == "access_token"
    
    def test_encode_refresh_token(self, jwt_handler, mock_user):
        """Probar la codificación de token de actualización."""
        token = jwt_handler.encode_refresh_token(mock_user)
        
        # Verificar que el token es una cadena
        assert isinstance(token, str)
        # Verificar que el token puede ser decodificado
        payload = jwt.decode(token, TEST_SECRET, algorithms=[TEST_ALGORITHM])
        assert payload["sub"] == mock_user.email
        assert payload["scope"] == "refresh_token"
    
    def test_encode_reset_token(self, jwt_handler, mock_user):
        """Probar la codificación de token de restablecimiento."""
        # Crear un diccionario con el email del usuario
        user_dict = {"email": mock_user.email}
        token = jwt_handler.encode_reset_token(user_dict)
        
        # Verificar que el token es una cadena
        assert isinstance(token, str)
        # Verificar que el token puede ser decodificado
        payload = jwt.decode(token, TEST_SECRET, algorithms=[TEST_ALGORITHM])
        assert payload["sub"] == mock_user.email
    
    def test_verify_reset_token(self, jwt_handler, mock_user):
        """Probar la verificación de token de restablecimiento."""
        # Crear un diccionario con el email del usuario
        user_dict = {"email": mock_user.email}
        token = jwt_handler.encode_reset_token(user_dict)
        
        # Verificar que el token es válido
        assert jwt_handler.verify_reset_token(token, mock_user.email) is True
        
        # Verificar que un token inválido no pasa la verificación
        assert jwt_handler.verify_reset_token("invalid_token", mock_user.email) is False
    
    def test_decode_token(self, jwt_handler, mock_user):
        """Probar la decodificación de token."""
        token = jwt_handler.encode_token(mock_user)
        decoded = jwt_handler.decode_token(token)
        
        # Verificar que el payload contiene la información correcta
        assert decoded["sub"] == mock_user.email
        assert decoded["user.name"] == mock_user.name
        assert decoded["user.id_number"] == mock_user.id_number
        assert decoded["user.role"] == mock_user.role_id
        assert decoded["user.status"] == mock_user.status
        assert decoded["user.is_verified"] == mock_user.is_verified
    
    def test_refresh_token_valid(self, jwt_handler, mock_user):
        """Probar la actualización de un token válido."""
        # Crear un token de actualización válido
        refresh_token = jwt_handler.encode_refresh_token(mock_user)
        
        # Configurar el mock para simular la búsqueda del usuario
        with patch('src.auth.jwt_handler.UserRepository') as mock_user_repo:
            mock_user_repo_instance = MagicMock()
            mock_user_repo.return_value = mock_user_repo_instance
            mock_user_repo_instance.get_user_by_email.return_value = mock_user
            
            # Configurar la sesión de base de datos
            jwt_handler.db = MagicMock()
            
            # Actualizar el token
            new_token = jwt_handler.refresh_token(refresh_token)
            
            # Verificar que se generó un nuevo token de acceso
            decoded = jwt.decode(new_token, TEST_SECRET, algorithms=[TEST_ALGORITHM])
            
            # Verificar que el nuevo token contiene la información correcta
            assert decoded["sub"] == mock_user.email
            assert decoded["scope"] == "access_token"
            assert decoded["user.name"] == mock_user.name
            assert decoded["user.id_number"] == mock_user.id_number
            assert decoded["user.role"] == mock_user.role_id
            assert decoded["user.status"] == mock_user.status
            assert decoded["user.is_verified"] == mock_user.is_verified 