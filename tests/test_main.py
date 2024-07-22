import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import get_db, SessionLocal, Base, Product
from app.products import ProductCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import Settings
from unittest.mock import patch
import os


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app.dependency_overrides[SessionLocal] = lambda: TestingSessionLocal()

test_settings = Settings()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")


def mock_scrape(*args, **kwargs):
    return [
        ProductCreate(product_title="Sample Product 1", product_price=100.0, path_to_image="images/sample1.jpg"),
        ProductCreate(product_title="Sample Product 2", product_price=200.0, path_to_image="images/sample2.jpg")
    ]

@patch("app.scraper.Scraper.scrape", side_effect=mock_scrape)
def test_scrape_endpoint(mock_scrape,test_db):
    response = client.get(
        "/scrape/?pages=1",
        headers={"Authorization": f"Bearer {test_settings.static_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["updated_count"] == 2

def test_invalid_token(test_db):
    response = client.get(
        "/scrape/?pages=1",
        headers={"Authorization": "Token invalid_token"}
    )
    assert response.status_code == 403
