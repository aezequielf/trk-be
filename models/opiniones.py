from pydantic import BaseModel
from typing import Optional

class Opinion(BaseModel):
    id: Optional[str] = None
    guiaid : str
    estrellas: int
    opinion: str
    userid: str
    nombre: str