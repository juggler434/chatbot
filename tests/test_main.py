from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app, get_db

engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )

TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
        )

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
            '/users',
            json={"email": "test@email.com", "password": "notgoodpassword"}
            )

    assert response.status_code == 200, response.text





