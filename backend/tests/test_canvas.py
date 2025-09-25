import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_snapshot():
    response = client.get("/canvas/snapshot")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

