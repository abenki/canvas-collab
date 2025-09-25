from fastapi import APIRouter, Depends
import redis.asyncio as redis
from app.core import config

router = APIRouter()

redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)

@router.get("/snapshot")
async def get_snapshot():
    """
    Retourne un snapshot simple du canvas sous forme de dict { "x,y": "#color" }.
    MVP: pas optimisé, juste pour tester.
    """
    data = await redis_client.hgetall("canvas")
    return data
