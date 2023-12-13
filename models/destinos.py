from pydantic import BaseModel
from typing import Optional

class Destino(BaseModel):
    id: Optional[str] = None
    lugar: str
    detalles: Optional[str] = None

    # detalles = [
    #     {
    #     "fecha": "23-12-2023",
    #     "guiaid" : "9797sa9df7as0f7as0",
    #     "empresa": "una empresa",

    #     }
    # ]

    