import pytest
from fastapi.testclient import TestClient

from just_chat.main.web import create_app


@pytest.fixture()
def client():
    app = create_app()
    client = TestClient(app)
    return client
