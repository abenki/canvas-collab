import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.pixel import PixelUpdate

client = TestClient(app)


@pytest.mark.asyncio
async def test_ws_endpoint():
    with client.websocket_connect("/ws") as websocket:
        update = PixelUpdate(x=10, y=10, color="#ff00cc", user_id="test_user")
        websocket.send_json(update.model_dump())
        response = websocket.receive_json()
        assert response is not None

