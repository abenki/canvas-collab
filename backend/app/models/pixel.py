from pydantic import BaseModel

class PixelUpdate(BaseModel):
    x: int
    y: int
    color: str   # ex: "#ff00cc"
    user_id: str
