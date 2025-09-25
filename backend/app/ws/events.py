from fastapi import WebSocket
import redis.asyncio as redis
import asyncio, json
from app.models.pixel import PixelUpdate
from app.core import config

redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)

async def handle_ws(ws: WebSocket):
    await ws.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("canvas_updates")

    async def listen_pubsub():
        async for message in pubsub.listen():
            if message["type"] == "message":
                await ws.send_text(message["data"])

    listener_task = asyncio.create_task(listen_pubsub())

    try:
        while True:
            msg = await ws.receive_json()
            update = PixelUpdate(**msg)

            # Cooldown check
            key = f"user:{update.user_id}:cooldown"
            if not await redis_client.set(key, "1", ex=config.COOLDOWN_SECONDS, nx=True):
                await ws.send_json({"error": "Cooldown active"})
                continue

            # Update canvas
            field = f"{update.x},{update.y}"
            await redis_client.hset("canvas", field, update.color)

            # Publish event
            payload = update.model_dump_json()
            await redis_client.publish("canvas_updates", payload)

    except Exception as e:
        print("WebSocket closed:", e)
    finally:
        listener_task.cancel()
        await pubsub.close()
