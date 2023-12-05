from pydantic import BaseModel
from typing import Optional

class Pcia(BaseModel):
    id: Optional[str] = None
    nombre: str
