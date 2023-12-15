from pydantic import BaseModel
from typing import Optional

class Destino(BaseModel):
    id: Optional[str] = None
    lugar: str
    area : str
    provincia : str
    detalles: Optional[str] = None

    # detalles = [
    #     {
    #     "fecha": "23-12-2023",
    #     "hora " : "08:00 am"
    #     "guiaid" : "9797sa9df7as0f7as0",
    #     "empresa": "una empresa",
    #     "descripcion" : "Breve descripción"
    #     },
    # ]

    