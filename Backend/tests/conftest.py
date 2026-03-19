import pytest
from fastapi.testclient import TestClient
from Backend.main import app

@pytest.fixture
def client():
    return TestClient(app)