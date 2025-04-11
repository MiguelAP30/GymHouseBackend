"""
Pruebas unitarias para el middleware de autenticación.
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.has_access import has_access
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

class TestHasAccess:
    """Clase para probar el middleware de autenticación."""
    
    @pytest.mark.asyncio
    async def test_has_access_invalid_token(self, jwt_handler):
        """Probar el acceso con un token inválido."""
        # Crear credenciales con un token inválido
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")
        
        # Verificar que se lanza una excepción al acceder con un token inválido
        with pytest.raises(HTTPException) as excinfo:
            await has_access(credentials)
        
        assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Invalid authentication credentials"
    
    @pytest.mark.asyncio
    async def test_has_access_expired_token(self, jwt_handler):
        """Probar el acceso con un token expirado."""
        # Crear un token expirado
        payload = {
            "exp": datetime.utcnow() - timedelta(hours=1),
            "iat": datetime.utcnow() - timedelta(hours=2),
            "sub": "test@example.com",
            "scope": "access_token",
            "user.name": "Test User",
            "user.id_number": "123456789",
            "user.role": 1,
            "user.status": True,
            "user.is_verified": True
        }
        token = jwt.encode(payload, TEST_SECRET, algorithm=TEST_ALGORITHM)
        
        # Crear credenciales con el token expirado
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        # Verificar que se lanza una excepción al acceder con un token expirado
        with pytest.raises(HTTPException) as excinfo:
            await has_access(credentials)
        
        assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Invalid authentication credentials"
    
    @pytest.mark.asyncio
    async def test_has_access_invalid_scope(self, jwt_handler, mock_user):
        """Probar el acceso con un token de scope inválido."""
        # Crear un token con scope inválido
        token = jwt_handler.encode_refresh_token(mock_user)  # Este es un token de actualización, no de acceso
        
        # Crear credenciales con el token de scope inválido
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        # Verificar que se lanza una excepción al acceder con un token de scope inválido
        with pytest.raises(HTTPException) as excinfo:
            await has_access(credentials)
        
        assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Invalid authentication credentials"
    
    @pytest.mark.asyncio
    async def test_has_access_missing_credentials(self):
        """Probar el acceso sin credenciales."""
        # Verificar que se lanza una excepción al acceder sin credenciales
        with pytest.raises(HTTPException) as excinfo:
            await has_access(None)
        
        assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Invalid authentication credentials" 