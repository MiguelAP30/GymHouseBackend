"""
Configuración y fixtures para las pruebas unitarias.
"""
import os
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Importar la aplicación FastAPI y modelos
from main import app
from src.config.database import Base

# Configurar variables de entorno para pruebas
os.environ["AUTH_SECRET_KEY"] = "test_secret_key"
os.environ["AUTH_ALGORITHM"] = "HS256"

# Crear un motor de base de datos en memoria para pruebas
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)

# Crear una sesión de base de datos para pruebas
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobreescribir la dependencia de base de datos
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Aplicar la sobreescritura de dependencias
from src.config.database import get_db
app.dependency_overrides[get_db] = override_get_db

# Crear un cliente de prueba
@pytest.fixture
def client():
    return TestClient(app)

# Crear una sesión de base de datos para pruebas
@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock para el repositorio de usuarios
@pytest.fixture
def mock_user_repository():
    with patch("src.repositories.user.UserRepository") as mock:
        yield mock

# Mock para el manejador JWT
@pytest.fixture
def mock_jwt_handler():
    with patch("src.auth.jwt_handler.JWTHandler") as mock:
        yield mock 