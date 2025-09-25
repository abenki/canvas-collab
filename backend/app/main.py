from fastapi import FastAPI, WebSocket
from app.api import canvas
from app.ws.events import handle_ws

app = FastAPI(title="Collaborative Canvas MVP")

app.include_router(canvas.router, prefix="/canvas", tags=["canvas"])

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await handle_ws(ws)
