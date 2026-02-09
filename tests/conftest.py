import pytest
from fastapi.testclient import TestClient
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db

from app.core.security import hash_password

DATABASE = "sqlite:///./test.db"

engine = create_engine(
    DATABASE, connect_args={"check_same_thread": False} 
)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def criar_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]





@pytest.fixture
def user_token(client):
    payload={
        "email": "teste@teste.com",
        "username": "teste",
        "password": "1234"
    }

    user_res = client.post("/auth/register", json=payload)

    login_data= {    
        "username": "teste@teste.com",
        "password": "1234"}
    
    response = client.post("/auth/login", data=login_data)

    print(response.json())


    return response.json()["access_token"]



