import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000
COOLDOWN_SECONDS = 300  # 5 minutes
