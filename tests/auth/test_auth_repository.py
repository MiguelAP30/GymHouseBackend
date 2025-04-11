"""
Pruebas unitarias para el repositorio de autenticación.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from datetime import datetime

from src.repositories.auth import AuthRepository
from src.schemas.user import User as UserCreateSchema, UserLogin as UserLoginSchema
from src.models.user import User as UserModel

@pytest.fixture
def auth_repo():
    """Fixture para crear una instancia del repositorio de autenticación."""
    return AuthRepository()

@pytest.fixture
def mock_user():
    """Fixture para crear un mock de usuario."""
    user = MagicMock()
    user.email = "test@example.com"
    user.password = "hashed_password"
    user.name = "Test User"
    user.id_number = "123456789"
    user.role_id = 1
    user.is_verified = True
    user.status = True
    return user

@pytest.fixture
def mock_user_repo():
    """Fixture para crear un mock del repositorio de usuarios."""
    with patch('src.repositories.auth.UserRepository') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_jwt_handler():
    """Fixture para crear un mock del manejador JWT."""
    with patch('src.repositories.auth.auth_handler') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_email_service():
    """Fixture para crear un mock del servicio de email."""
    with patch('src.repositories.auth.EmailService') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_db(self):
    mock = MagicMock()
    mock.query.return_value.filter.return_value.first.return_value = None
    return mock

@pytest.fixture
def mock_user_model(self):
    return MagicMock(spec=UserModel)

class TestAuthRepository:
    """Pruebas para el repositorio de autenticación."""

    @patch('src.repositories.auth.SessionLocal')
    def test_register_user_existing(self, mock_session_local, auth_repo):
        """Probar el registro de un usuario que ya existe."""
        # Configurar los mocks
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_session_local.return_value = mock_db

        # Crear datos de usuario
        user_data = UserCreateSchema(
            email="test@example.com",
            password="password123",
            name="Test User",
            id_number="123456789",
            user_name="testuser",
            phone="1234567890",
            address="Test Address",
            birth_date=datetime.now().isoformat(),
            gender="M"
        )

        # Verificar que se lanza una excepción
        with pytest.raises(HTTPException) as excinfo:
            auth_repo.register_user(user_data)

        assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
        assert excinfo.value.detail == "El usuario ya existe"

    @patch('src.repositories.auth.SessionLocal')
    def test_verify_email_user_not_found(self, mock_session_local, auth_repo):
        """Probar la verificación del correo electrónico de un usuario que no existe."""
        # Configurar los mocks
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_session_local.return_value = mock_db

        # Verificar que se lanza una excepción
        with pytest.raises(HTTPException) as excinfo:
            auth_repo.verify_email("test@example.com", "123456")

        assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
        assert excinfo.value.detail == "Usuario no encontrado"

    @patch('src.repositories.auth.SessionLocal')
    def test_verify_email_invalid_code(self, mock_session_local, auth_repo):
        """Probar la verificación del correo electrónico con un código inválido."""
        # Configurar los mocks
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_user.is_verified = False
        mock_user.verification_code = "123456"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_session_local.return_value = mock_db

        # Verificar que se lanza una excepción
        with pytest.raises(HTTPException) as excinfo:
            auth_repo.verify_email("test@example.com", "654321")

        assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
        assert excinfo.value.detail == "Código de verificación inválido"

    @patch('src.repositories.auth.SessionLocal')
    def test_change_password_user_not_found(self, mock_session_local, auth_repo):
        """Probar el cambio de contraseña de un usuario que no existe."""
        # Configurar los mocks
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_session_local.return_value = mock_db

        # Verificar que se lanza una excepción
        with pytest.raises(HTTPException) as excinfo:
            auth_repo.change_password(
                email="test@example.com",
                current_password="password123",
                new_password="new_password"
            )

        assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
        assert excinfo.value.detail == "Usuario no encontrado"

    @patch('src.repositories.auth.SessionLocal')
    @patch('src.repositories.auth.auth_handler')
    def test_change_password_invalid_current(self, mock_auth_handler, mock_session_local, auth_repo):
        """Probar el cambio de contraseña con la contraseña actual incorrecta."""
        # Configurar los mocks
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_user.password = "hashed_password"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_session_local.return_value = mock_db
        mock_auth_handler.verify_password.return_value = False

        # Verificar que se lanza una excepción
        with pytest.raises(HTTPException) as excinfo:
            auth_repo.change_password(
                email="test@example.com",
                current_password="wrong_password",
                new_password="new_password"
            )

        assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Contraseña actual incorrecta"

    @patch('src.repositories.auth.SessionLocal')
    def test_reset_password_invalid_code(self, mock_session_local, auth_repo):
        """Probar el restablecimiento de contraseña con un código inválido."""
        # Configurar los mocks
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_user.verification_code = "123456"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_session_local.return_value = mock_db

        # Verificar que se lanza una excepción
        with pytest.raises(HTTPException) as excinfo:
            auth_repo.reset_password(
                email="test@example.com",
                new_password="new_password",
                reset_code="654321"
            )

        assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST 